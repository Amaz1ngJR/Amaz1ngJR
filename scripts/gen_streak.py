#!/usr/bin/env python3
"""从 GitHub GraphQL API 拉取贡献日历，计算连续提交天数并生成 SVG 卡片。

替代原来依赖的 github-readme-streak-stats.herokuapp.com。
需要环境变量 GH_TOKEN（有 public_repo 权限即可）与 GH_USER。
"""

import json
import os
import sys
import urllib.error
import urllib.request
from datetime import date, datetime, timedelta

API = "https://api.github.com/graphql"

# tokyonight 配色，与 README 其他卡片一致
BG = "#1a1b27"
TEXT = "#a9b1d6"
ACCENT = "#70a5fd"
FLAME = "#ff7a93"
MUTED = "#565f89"

QUERY_CREATED = """
query($login: String!) {
  user(login: $login) { createdAt }
}
"""

QUERY_CAL = """
query($login: String!, $from: DateTime!, $to: DateTime!) {
  user(login: $login) {
    contributionsCollection(from: $from, to: $to) {
      contributionCalendar {
        weeks {
          contributionDays { date contributionCount }
        }
      }
    }
  }
}
"""


def gql(token, query, variables):
    req = urllib.request.Request(
        API,
        data=json.dumps({"query": query, "variables": variables}).encode(),
        headers={
            "Authorization": f"bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "streak-card-generator",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            payload = json.load(resp)
    except urllib.error.HTTPError as exc:
        sys.exit(f"GitHub API HTTP {exc.code}: {exc.read()[:300]!r}")
    except urllib.error.URLError as exc:
        sys.exit(f"GitHub API 请求失败: {exc.reason}")
    if "errors" in payload:
        sys.exit(f"GraphQL 报错: {payload['errors']}")
    if not payload.get("data", {}).get("user"):
        sys.exit("GraphQL 未返回 user，检查 GH_USER 与 token 权限")
    return payload["data"]


def fetch_contributions(token, user):
    """贡献日历单次查询最多覆盖一年，按年分段拉全部历史。"""
    created = gql(token, QUERY_CREATED, {"login": user})["user"]["createdAt"]
    start = datetime.strptime(created[:10], "%Y-%m-%d").date()
    today = date.today()

    days = {}
    cursor = start
    while cursor <= today:
        chunk_end = min(cursor + timedelta(days=364), today)
        data = gql(
            token,
            QUERY_CAL,
            {
                "login": user,
                "from": f"{cursor.isoformat()}T00:00:00Z",
                "to": f"{chunk_end.isoformat()}T23:59:59Z",
            },
        )
        weeks = data["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]
        for week in weeks:
            for day in week["contributionDays"]:
                days[day["date"]] = day["contributionCount"]
        cursor = chunk_end + timedelta(days=1)
    return days, start


def compute(days):
    """返回 (总贡献, 当前连续天数, 当前区间, 最长连续天数, 最长区间)。"""
    today = date.today()
    dated = sorted((datetime.strptime(d, "%Y-%m-%d").date(), c) for d, c in days.items())
    dated = [(d, c) for d, c in dated if d <= today]

    total = sum(c for _, c in dated)

    longest = cur = 0
    longest_span = cur_span = (None, None)
    for d, count in dated:
        if count > 0:
            cur = cur + 1 if cur else 1
            cur_span = (cur_span[0] or d, d)
            if cur > longest:
                longest, longest_span = cur, cur_span
        else:
            cur, cur_span = 0, (None, None)

    # 今天还没提交不算断档，从昨天往回数
    current, current_span = 0, (None, None)
    idx = len(dated) - 1
    if idx >= 0 and dated[idx][0] == today and dated[idx][1] == 0:
        idx -= 1
    end = None
    while idx >= 0 and dated[idx][1] > 0:
        current += 1
        end = end or dated[idx][0]
        current_span = (dated[idx][0], end)
        idx -= 1

    return total, current, current_span, longest, longest_span


def fmt_span(span):
    if not span[0]:
        return "—"
    fmt = "%Y.%m.%d"
    if span[0] == span[1]:
        return span[0].strftime(fmt)
    return f"{span[0].strftime(fmt)} - {span[1].strftime(fmt)}"


def render(total, current, current_span, longest, longest_span, since):
    cols = [
        ("Total Contributions", str(total), f"{since.strftime('%Y.%m.%d')} - Present", TEXT),
        ("Current Streak", str(current), fmt_span(current_span), FLAME),
        ("Longest Streak", str(longest), fmt_span(longest_span), TEXT),
    ]
    w, h, cw = 495, 195, 165
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" fill="none" role="img" '
        f'aria-label="GitHub 连续提交统计：总贡献 {total}，当前连续 {current} 天，最长连续 {longest} 天">',
        "<style>"
        ".num{font:700 28px -apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif}"
        ".lbl{font:400 14px -apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif}"
        ".rng{font:400 11px -apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif}"
        "</style>",
        f'<rect width="{w}" height="{h}" rx="6" fill="{BG}"/>',
    ]
    for i, (label, value, rng, color) in enumerate(cols):
        cx = cw // 2 + i * cw
        parts.append(f'<text x="{cx}" y="62" class="num" fill="{color}" text-anchor="middle">{value}</text>')
        parts.append(f'<text x="{cx}" y="96" class="lbl" fill="{ACCENT}" text-anchor="middle">{label}</text>')
        parts.append(f'<text x="{cx}" y="120" class="rng" fill="{MUTED}" text-anchor="middle">{rng}</text>')
        if i:
            x = i * cw
            parts.append(f'<line x1="{x}" y1="40" x2="{x}" y2="150" stroke="{MUTED}" stroke-opacity="0.35"/>')
    parts.append("</svg>")
    return "\n".join(parts)


def main():
    token = os.environ.get("GH_TOKEN")
    user = os.environ.get("GH_USER")
    if not token or not user:
        sys.exit("缺少环境变量 GH_TOKEN 或 GH_USER")

    out = sys.argv[1] if len(sys.argv) > 1 else "metrics/streak.svg"
    days, since = fetch_contributions(token, user)
    total, current, current_span, longest, longest_span = compute(days)

    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(render(total, current, current_span, longest, longest_span, since))

    print(f"已写入 {out}")
    print(f"总贡献 {total} / 当前连续 {current} 天 / 最长连续 {longest} 天")


if __name__ == "__main__":
    main()
