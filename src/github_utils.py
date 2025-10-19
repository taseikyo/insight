#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2025-10-19 14:28:03
# @Author  : Lewis Tian (taseikyo@gmail.com)
# @Link    : github.com/taseikyo
# @Version : 3.12.3


from github import Github
from github.Issue import Issue
from github.IssueComment import IssueComment

from . import logger_utls
from . import parser

LABEL_DICT = {
    "alipay": {
        "parser": None,
    },
    "xiaoheihe": {
        "parser": None,
    },
    "weibo": {
        "parser": None,
    },
    "douyin": {
        "parser": parser.douyin_parser,
    },
}


def login(token: str) -> Github:
    return Github(token)


def get_me(user: Github) -> str:
    return user.get_user().login


def is_me(comment: IssueComment, me: str) -> bool:
    return comment.user.login == me


def get_issue(
    logger: logger_utls.Logger, github_token: str, repo_name: str, issue_label_name: str
) -> list[Issue]:
    process_issues = []
    if not github_token or not repo_name or not issue_label_name:
        logger.error("github_token, repo_name, issue_label_name is required")
        return process_issues

    logger.info(
        f"Start fetching issues from repo: {repo_name} with label: {issue_label_name}"
    )

    labels = LABEL_DICT.get(issue_label_name, {})
    if not labels:
        logger.error(f"No labels found for issue_label_name: {issue_label_name}")
        return process_issues
    u = login(github_token)
    me = get_me(u)
    issues = u.get_repo(repo_name).get_issues(labels=[issue_label_name])
    if not issues:
        logger.warning(f"No issues found for label: {issue_label_name}")
        return process_issues

    for issue in issues:
        comments = issue.get_comments()
        for comment in comments:
            if not is_me(comment, me):
                continue
            process_issues.append(issue)

    return process_issues
