#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2025-10-19 14:27:23
# @Author  : Lewis Tian (taseikyo@gmail.com)
# @Link    : github.com/taseikyo
# @Version : 3.12.3

import argparse

import pytz

from src.github_utils import get_issue
from src.github_utils import LABEL_DICT
from src.logger_utls import Logger

BASE_HEADER = "| ID | Crteate / Update | Content | \n| ---- | ---- | ---- | \n"
SH_TZ = pytz.timezone("Asia/Shanghai")


def update_readme(lines: list[str], label: str) -> None:
    if len(lines) == 0:
        return

    readme_path = "README.md"
    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    start_marker = f"<!--StartSection:{label}-->"
    end_marker = f"<!--EndSection:{label}-->"

    start_index = content.find(start_marker)
    end_index = content.find(end_marker)

    if start_index == -1 or end_index == -1:
        raise ValueError(f"Markers for label {label} not found in README.md")

    new_section = f"{start_marker}\n" f"{BASE_HEADER}" + "".join(lines)

    new_content = content[:start_index] + new_section + content[end_index:]

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(new_content)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--github_token", help="github_token", default="", required=True
    )
    parser.add_argument("--repo_name", help="repo_name", default="", required=True)
    parser.add_argument(
        "--issue_label_name", help="issue_label_name", default="", required=True
    )
    options = parser.parse_args()

    logger = Logger()
    issues = get_issue(
        logger,
        options.github_token,
        options.repo_name,
        options.issue_label_name,
    )

    logger.info(f"Fetched {len(issues)} issues.")

    lines = []
    uniq_ids = set()
    uniq_issue_ids = set()
    for issue in issues:
        if issue.id in uniq_issue_ids:
            continue
        uniq_issue_ids.add(issue.id)
        label = issue.labels[0].name if issue.labels else ""
        logger.info(
            f"Issue Title: {issue.title}, Number: {issue.number}, Label: {label}, Counts: {issue.comments}"
        )
        for comment in reversed(issue.get_comments()):
            if comment.id in uniq_ids:
                continue
            uniq_ids.add(comment.id)
            # 替换评论所有回车为空格
            body = " ".join(comment.body.splitlines())
            ct = comment.created_at.astimezone(SH_TZ).strftime("%Y-%m-%d %H:%M:%S")
            ut = comment.updated_at.astimezone(SH_TZ).strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"  Comment User {comment.user.login}, Create Time: {ct}")
            logger.info(f"  Comment ID: {comment.id}")
            logger.info(f"  Comment Body: {body}")

            parser_func = LABEL_DICT[label].get("parser")
            if parser_func:
                body = parser_func(logger, body)

            line = f"| [{comment.id}]({comment.html_url}) | {ct} /<br /> {ut} |<pre>{body}</pre> | \n"
            lines.append(line)
            logger.info(line)

    update_readme(lines, options.issue_label_name)


if __name__ == "__main__":
    main()
