""" 

MIT License 

  

Copyright (c) 2022 ABISHNOI69 

  

Permission is hereby granted, free of charge, to any person obtaining a copy 

of this software and associated documentation files (the "Software"), to deal 

in the Software without restriction, including without limitation the rights 

to use, copy, modify, merge, publish, distribute, sublicense, and/or sell 

copies of the Software, and to permit persons to whom the Software is 

furnished to do so, subject to the following conditions: 

  

The above copyright notice and this permission notice shall be included in all 

copies or substantial portions of the Software. 

  

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 

IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 

FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 

AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 

LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 

OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 

SOFTWARE. 

""" 

  

# ""DEAR PRO PEOPLE,  DON'T REMOVE & CHANGE THIS LINE 

# TG :- @Abishnoi1m 

#     UPDATE   :- Abishnoi_bots 

#     GITHUB :- ABISHNOI69 "" 

  

import html 

  

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Update 

from telegram.error import BadRequest 

from telegram.ext import CallbackContext, CallbackQueryHandler 

from telegram.utils.helpers import mention_html 

  

import Exon.modules.sql.approve_sql as sql 

from Exon import DRAGONS, dispatcher 

from Exon.modules.disable import DisableAbleCommandHandler 

from Exon.modules.helper_funcs.chat_status import user_admin 

from Exon.modules.helper_funcs.extraction import extract_user 

from Exon.modules.log_channel import loggable 

  

  

@loggable 

@user_admin 

def approve(update, context): 

    message = update.effective_message 

    chat_title = message.chat.title 

    chat = update.effective_chat 

    args = context.args 

    user = update.effective_user 

    user_id = extract_user(message, args) 

    if not user_id: 

        message.reply_text( 

            "I don't know who you're talking about, you're going to need to specify a user!", 

        ) 

        return "" 

    try: 

        member = chat.get_member(user_id) 

    except BadRequest: 

        return "" 

    if member.status in ("administrator", "creator"): 

        message.reply_text( 

            "User is already admin - locks, blocklists, and antiflood already don't apply to them.", 

        ) 

        return "" 

    if sql.is_approved(message.chat_id, user_id): 

        message.reply_text( 

            f"[{member.user['first_name']}](tg://user?id={member.user['id']}) Is already approved in {chat_title}.", 

            parse_mode=ParseMode.MARKDOWN, 

        ) 

        return "" 

    sql.approve(message.chat_id, user_id) 

    message.reply_text( 

        f"[{member.user['first_name']}](tg://user?id={member.user['id']}) has been approved in {chat_title}! they will now be ignored by automated admin actions like locks, blocklists, and antiflood.", 

        parse_mode=ParseMode.MARKDOWN, 

    ) 

    log_message = ( 

        f"<b>{html.escape(chat.title)}:</b>\n" 

        f"#APPROVED\n" 

        f"<b>ADMIN:</b> {mention_html(user.id, user.first_name)}\n" 

        f"<b>User:</b> {mention_html(member.user.id, member.user.first_name)}" 

    ) 

  

    return log_message 

  

  

@loggable 

@user_admin 

def disapprove(update, context): 

    message = update.effective_message 

    chat_title = message.chat.title 

    chat = update.effective_chat 

    args = context.args 

    user = update.effective_user 

    user_id = extract_user(message, args) 

    if not user_id: 

        message.reply_text( 

            "I don't know who you're talking about, you're going to need to specify a user!", 

        ) 

        return "" 

    try: 

        member = chat.get_member(user_id) 

    except BadRequest: 

        return "" 

    if member.status in ("administrator", "creator"): 

        message.reply_text("This user is an admin, they can't be unapproved.") 

        return "" 

    if not sql.is_approved(message.chat_id, user_id): 

        message.reply_text(f"{member.user['first_name']} Isn't approved yet!") 

        return "" 

    sql.disapprove(message.chat_id, user_id) 

    message.reply_text( 

        f"{member.user['first_name']} is no longer approved in {chat_title}.", 

    ) 

    log_message = ( 

        f"<b>{html.escape(chat.title)}:</b>\n" 

        f"#UNAPPROVED\n" 

        f"<b>ADMIN:</b> {mention_html(user.id, user.first_name)}\n" 

        f"<b>User:</b> {mention_html(member.user.id, member.user.first_name)}" 

    ) 

  

    return log_message 

  

  

@user_admin 

def approved(update, context): 

    message = update.effective_message 

    chat_title = message.chat.title 

    chat = update.effective_chat 

    msg = "The following user's are approved.\n" 

    approved_users = sql.list_approved(message.chat_id) 

    for i in approved_users: 

        member = chat.get_member(int(i.user_id)) 

        msg += f"x `{i.user_id}`: {member.user['first_name']}\n" 

    if msg.endswith("Approved.\n"): 

        message.reply_text(f"No users are approved in {chat_title}.") 

        return "" 

    message.reply_text(msg, parse_mode=ParseMode.MARKDOWN) 

  

  

@user_admin 

def approval(update, context): 

    message = update.effective_message 

    chat = update.effective_chat 

    args = context.args 

    user_id = extract_user(message, args) 

    member = chat.get_member(int(user_id)) 

    if not user_id: 

        message.reply_text( 

            "I don't know who you're talking about, you're going to need to specify a user!", 

        ) 

        return "" 

    if sql.is_approved(message.chat_id, user_id): 

        message.reply_text( 

            f"{member.user['first_name']} is an approved user. locks, antiflood, and blocklists won't apply to them.", 

        ) 

    else: 

        message.reply_text( 

            f"{member.user['first_name']} is not an approved user. they are affected by normal commands.", 

        ) 

  

  

def unapproveall(update: Update, context: CallbackContext): 

    chat = update.effective_chat 

    user = update.effective_user 

    member = chat.get_member(user.id) 

    if member.status != "creator" and user.id not in DRAGONS: 

        update.effective_message.reply_text( 

            "Only the chat owner can unapprove all users at once.", 

        ) 

    else: 

        buttons = InlineKeyboardMarkup( 

            [ 

                [ 

                    InlineKeyboardButton( 

                        text="Unapprove all users", 

                        callback_data="unapproveall_user", 

                    ), 

                ], 

                [ 

                    InlineKeyboardButton( 

                        text="cancel", 

                        callback_data="unapproveall_cancel", 

                    ), 

                ], 

            ], 

        ) 

        update.effective_message.reply_text( 

            f"Are you sure you would like to unapprove all users in {chat.title}? this action cannot be undone.", 

            reply_markup=buttons, 

            parse_mode=ParseMode.MARKDOWN, 

        ) 

  

  

def unapproveall_btn(update: Update, context: CallbackContext): 

    query = update.callback_query 

    chat = update.effective_chat 

    message = update.effective_message 

    member = chat.get_member(query.from_user.id) 

    if query.data == "unapproveall_user": 

        if member.status == "creator" or query.from_user.id in DRAGONS: 

            approved_users = sql.list_approved(chat.id) 

            users = [int(i.user_id) for i in approved_users] 

            for user_id in users: 

                sql.disapprove(chat.id, user_id) 

            message.edit_text("Successfully unapproved all user in this chat.") 

            return 

  

        if member.status == "administrator": 

            query.answer("Only owner of the chat can do this.") 

  

        if member.status == "member": 

            query.answer("You need to be admin to do this.") 

    elif query.data == "unapproveall_cancel": 

        if member.status == "creator" or query.from_user.id in DRAGONS: 

            message.edit_text("Removing of all approved users has been cancelled.") 

            return "" 

        if member.status == "administrator": 

            query.answer("Only owner of the chat can do this.") 

        if member.status == "member": 

            query.answer("You need to be admin to do this.") 

  

  

APPROVE = DisableAbleCommandHandler(["approve", "free"], approve, run_async=True) 

DISAPPROVE = DisableAbleCommandHandler("unapprove", disapprove, run_async=True) 

APPROVED = DisableAbleCommandHandler("approved", approved, run_async=True) 

APPROVAL = DisableAbleCommandHandler("approval", approval, run_async=True) 

UNAPPROVEALL = DisableAbleCommandHandler("unapproveall", unapproveall, run_async=True) 

UNAPPROVEALL_BTN = CallbackQueryHandler( 

    unapproveall_btn, pattern=r"unapproveall_.*", run_async=True 

) 

  

dispatcher.add_handler(APPROVE) 

dispatcher.add_handler(DISAPPROVE) 

dispatcher.add_handler(APPROVED) 

dispatcher.add_handler(APPROVAL) 

dispatcher.add_handler(UNAPPROVEALL) 

dispatcher.add_handler(UNAPPROVEALL_BTN) 

  

__mod_name__ = "Approval" 

  

  

# foR HELP MENU 

# """ 

from Exon.modules.language import gs 

  

  

def get_help(chat): 

    return gs(chat, "approve_help") 

  

  

# """ 

  

  

__command_list__ = ["approve", "unapprove", "approved", "approval"] 

__handlers__ = [APPROVE, DISAPPROVE, APPROVED, APPROVAL] 

 
