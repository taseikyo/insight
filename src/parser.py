# -*- coding: utf-8 -*-
# @Date    : 2025-10-19 20:19:01
# @Author  : Lewis Tian (taseikyo@gmail.com)
# @Link    : github.com/taseikyo
# @Version : 3.12.3

from . import logger_utls

DOUYIN_TEMPLATE = "<table max-width='600px'><tr><th>投稿</th><th>{Link}</th></tr><tr><td>类型</td><td>{Type}</td></tr><tr><th>评论者</th><td>{User}</td></tr><tr><th>评论头像</th><td>{Avatar}</td></tr><tr><th>评论内容</th><td>{Content}</td></tr></table>"

def douyin_parser(logger: logger_utls.Logger, comment_body: str) -> str:
    """
    解析抖音评论内容，提取相关信息并格式化为表格形式。
    # source
    https://www.douyin.com/video/7434916752632450344
    # type
    comment
    # user
    https://www.douyin.com/user/MS4wLjABAAAAM_GrKfgTd5Z7TxbFpR2uzLQ9H7I5O9AH6rIJIt-ZRBs
    # nickname
    迷途小书童
    # avatar
    https://p3-pc.douyinpic.com/img/a6400002ef87687e044a~c5_300x300.jpeg
    # content
    平淡的言语中，似乎过去那些苦难轻舟已过万重山，春秋笔法，谁又知道只言片语里，是多少个汗水泪水交织的日日夜夜。
    """
    source_idx = comment_body.find("# source")
    type_idx = comment_body.find("# type")
    user_idx = comment_body.find("# user")
    avatar_idx = comment_body.find("# avatar")
    nickname_idx = comment_body.find("# nickname")
    content_idx = comment_body.find("# content")

    logger.info(f"source index: {source_idx}, type index: {type_idx}, user index: {user_idx}, avatar index: {avatar_idx}, nickname index: {nickname_idx}, content index: {content_idx}")

    source = comment_body[source_idx + len("# source"):type_idx].strip()
    dtype = comment_body[type_idx + len("# type"):user_idx].strip()
    user = comment_body[user_idx + len("# user"):nickname_idx].strip()
    nickname = comment_body[nickname_idx + len("# nickname"):avatar_idx].strip()
    avatar = comment_body[avatar_idx + len("# avatar"):content_idx].strip()
    content = comment_body[content_idx + len("# content"):].strip()

    parsed_content = DOUYIN_TEMPLATE.format(Link=source, Type=dtype, User=f"[{nickname}]({user})", Avatar=avatar, Content=content)
    logger.info(f"Parsed content: {parsed_content}")
    return parsed_content