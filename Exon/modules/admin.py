import asyncio 

import html 

import os 

  

from telegram import ParseMode, Update 

from telegram.error import BadRequest 

from telegram.ext import CallbackContext, CommandHandler 

from telegram.utils.helpers import mention_html 

  

from Exon import DRAGONS, dispatcher 

from Exon.modules.disable import DisableAbleCommandHandler 

from Exon.modules.helper_funcs.admin_rights import user_can_changeinfo 

from Exon.modules.helper_funcs.alternate import send_message 

from Exon.modules.helper_funcs.chat_status import ( 

    ADMIN_CACHE, 

    bot_admin, 

    can_pin, 

    can_promote, 

    connection_status, 

    user_admin, 

) 

from Exon.modules.helper_funcs.extraction import ( 

    extract_user, 

    extract_user_and_text, 

) 

from Exon.modules.log_channel import loggable 

  

  

@bot_admin 

@user_admin 

def set_sticker(update: Update, context: CallbackContext): 

    msg = update.effective_message 

    chat = update.effective_chat 

    user = update.effective_user 

  

    if user_can_changeinfo(chat, user, context.bot.id) is False: 

        return msg.reply_text( 

            "• You don't have permissions to change group info!" 

        ) 

  

    if msg.reply_to_message: 

        if not msg.reply_to_message.sticker: 

            return msg.reply_text( 

                "• Reply to a sticker to set it as group sticker pack !" 

            ) 

        stkr = msg.reply_to_message.sticker.set_name 

        try: 

            context.bot.set_chat_sticker_set(chat.id, stkr) 

            msg.reply_text(f"• successfully set group stickers in {chat.title}!") 

        except BadRequest as excp: 

            if excp.message == "Participants_too_few": 

                return msg.reply_text( 

                    "• your group needs minimum 100 members for setting a sticker pack as group sticker pack !" 

                ) 

            msg.reply_text(f"Error ! {excp.message}.") 

    else: 

        msg.reply_text("• Reply to a sticker to set it as group sticker pack !") 

  

  

@bot_admin 

@user_admin 

def setchatpic(update: Update, context: CallbackContext): 

    chat = update.effective_chat 

    msg = update.effective_message 

    user = update.effective_user 

  

    if user_can_changeinfo(chat, user, context.bot.id) is False: 

        msg.reply_text("• You don't have permissions to change group info !") 

        return 

  

    if msg.reply_to_message: 

        if msg.reply_to_message.photo: 

            pic_id = msg.reply_to_message.photo[-1].file_id 

        elif msg.reply_to_message.document: 

            pic_id = msg.reply_to_message.document.file_id 

        else: 

            msg.reply_text("• You can only set photos as group pfp !") 

            return 

        dlmsg = msg.reply_text("• changing group's profile pic...") 

        tpic = context.bot.get_file(pic_id) 

        tpic.download("gpic.png") 

        try: 

            with open("gpic.png", "rb") as chatp: 

                context.bot.set_chat_photo(int(chat.id), photo=chatp) 

                msg.reply_text("• successfully set group profile pic !") 

        except BadRequest as excp: 

            msg.reply_text(f"Error ! {excp.message}") 

        finally: 

            dlmsg.delete() 

            if os.path.isfile("gpic.png"): 

                os.remove("gpic.png") 

    else: 

        msg.reply_text("• Reply to a photo or file to set it as group profile pic !") 

  

  

@bot_admin 

@user_admin 

def rmchatpic(update: Update, context: CallbackContext): 

    chat = update.effective_chat 

    msg = update.effective_message 

    user = update.effective_user 

  

    if user_can_changeinfo(chat, user, context.bot.id) is False: 

        msg.reply_text("• You don't have permissions to change group info !") 

        return 

    try: 

        context.bot.delete_chat_photo(int(chat.id)) 

        msg.reply_text("• successfully deleted group's default profile pic !") 

    except BadRequest as excp: 

        msg.reply_text(f"Error ! {excp.message}.") 

        return 

  

  

@bot_admin 

@user_admin 

def set_desc(update: Update, context: CallbackContext): 

    msg = update.effective_message 

    chat = update.effective_chat 

    user = update.effective_user 

  

    if user_can_changeinfo(chat, user, context.bot.id) is False: 

        return msg.reply_text( 

            "• You don't have permissions to change group info !" 

        ) 

  

    tesc = msg.text.split(None, 1) 

    if len(tesc) >= 2: 

        desc = tesc[1] 

    else: 

        return msg.reply_text("• Wtf, you want to set an empty description !") 

    try: 

        if len(desc) > 255: 

            return msg.reply_text( 

                "• Description must be less than 255 words or characters !" 

            ) 

        context.bot.set_chat_description(chat.id, desc) 

        msg.reply_text(f"• successfully updated chat description in {chat.title}!") 

    except BadRequest as excp: 

        msg.reply_text(f"Error ! {excp.message}.") 

  

  

@bot_admin 

@user_admin 

def setchat_title(update: Update, context: CallbackContext): 

    chat = update.effective_chat 

    msg = update.effective_message 

    user = update.effective_user 

    args = context.args 

  

    if user_can_changeinfo(chat, user, context.bot.id) is False: 

        msg.reply_text("• You don't have permissions to change group info baby !") 

        return 

  

    title = " ".join(args) 

    if not title: 

        msg.reply_text("• Enter some text to set it as new chat title !") 

        return 

  

    try: 

        context.bot.set_chat_title(int(chat.id), str(title)) 

        msg.reply_text( 

            f"• successfully set <b>{title}</b> as new chat title !", 

            parse_mode=ParseMode.HTML, 

        ) 

    except BadRequest as excp: 

        msg.reply_text(f"Error ! {excp.message}.") 

        return 

  

  

@connection_status 

@bot_admin 

@can_promote 

@user_admin 

@loggable 

def promote(update: Update, context: CallbackContext) -> str: 

    bot = context.bot 

    args = context.args 

  

    message = update.effective_message 

    chat = update.effective_chat 

    user = update.effective_user 

  

    promoter = chat.get_member(user.id) 

  

    if ( 

        not (promoter.can_promote_members or promoter.status == "creator") 

        and user.id not in DRAGONS 

    ): 

        message.reply_text("• You don't have permissions to add new admins !") 

        return 

  

    user_id = extract_user(message, args) 

  

    if not user_id: 

        message.reply_text( 

            "• I don't know who's that user, never seen him in any of the chats where i am present !", 

        ) 

        return 

  

    try: 

        user_member = chat.get_member(user_id) 

    except: 

        return 

  

    if user_member.status in ("administrator", "creator"): 

        message.reply_text("• According to me that user is already an admin here !") 

        return 

  

    if user_id == bot.id: 

        message.reply_text( 

            "• I can't promote myself, my owner didn't told me to do so." 

        ) 

        return 

  

    # set same perms as bot - bot can't assign higher perms than itself! 

    bot_member = chat.get_member(bot.id) 

  

    try: 

        bot.promoteChatMember( 

            chat.id, 

            user_id, 

            can_change_info=bot_member.can_change_info, 

            can_post_messages=bot_member.can_post_messages, 

            can_edit_messages=bot_member.can_edit_messages, 

            can_delete_messages=bot_member.can_delete_messages, 

            can_invite_users=bot_member.can_invite_users, 

            can_manage_voice_chats=bot_member.can_manage_voice_chats, 

            can_pin_messages=bot_member.can_pin_messages, 

        ) 

    except BadRequest as err: 

        if err.message == "User_not_mutual_contact": 

            message.reply_text("• As i can see that user is not present here.") 

        else: 

            message.reply_text( 

                "• something went wrong, maybe someone promoted that user before me." 

            ) 

        return 

  

    bot.sendMessage( 

        chat.id, 

        f"<b>• Promoting a user in</b> {chat.title}\n\nPromoted : {mention_html(user_member.user.id, user_member.user.first_name)}\nPromoter : {mention_html(user.id, user.first_name)}", 

        parse_mode=ParseMode.HTML, 

    ) 

  

    log_message = ( 

        f"<b>{html.escape(chat.title)}:</b>\n" 

        f"#Promoted\n" 

        f"<b>Promoter :</b> {mention_html(user.id, user.first_name)}\n" 

        f"<b>User :</b> {mention_html(user_member.user.id, user_member.user.first_name)}" 

    ) 

  

    return log_message 

  

  

@connection_status 

@bot_admin 

@can_promote 

@user_admin 

@loggable 

def lowpromote(update: Update, context: CallbackContext) -> str: 

    bot = context.bot 

    args = context.args 

  

    message = update.effective_message 

    chat = update.effective_chat 

    user = update.effective_user 

  

    promoter = chat.get_member(user.id) 

  

    if ( 

        not (promoter.can_promote_members or promoter.status == "creator") 

        and user.id not in DRAGONS 

    ): 

        message.reply_text("• You don't have permissions to add new admins !") 

        return 

  

    user_id = extract_user(message, args) 

  

    if not user_id: 

        message.reply_text( 

            "• I don't know who's that user, never seen him in any of the chats where i am present !", 

        ) 

        return 

  

    try: 

        user_member = chat.get_member(user_id) 

    except: 

        return 

  

    if user_member.status in ("administrator", "creator"): 

        message.reply_text("• According to me that user is already an admin here !") 

        return 

  

    if user_id == bot.id: 

        message.reply_text( 

            "• I can't promote myself, my owner didn't told me to do so." 

        ) 

        return 

  

    # set same perms as bot - bot can't assign higher perms than itself! 

    bot_member = chat.get_member(bot.id) 

  

    try: 

        bot.promoteChatMember( 

            chat.id, 

            user_id, 

            can_delete_messages=bot_member.can_delete_messages, 

            can_invite_users=bot_member.can_invite_users, 

            can_pin_messages=bot_member.can_pin_messages, 

        ) 

    except BadRequest as err: 

        if err.message == "User_not_mutual_contact": 

            message.reply_text("• As i can see that user is not present here.") 

        else: 

            message.reply_text( 

                "• something went wrong, maybe someone promoted that user before me." 

            ) 

        return 

  

    bot.sendMessage( 

        chat.id, 

        f"<b>• Low promoting a user in </b>{chat.title}\n\n<b>Promoted :</b> {mention_html(user_member.user.id, user_member.user.first_name)}\nPromoter : {mention_html(user.id, user.first_name)}", 

        parse_mode=ParseMode.HTML, 

    ) 

  

    log_message = ( 

        f"<b>{html.escape(chat.title)}:</b>\n" 

        f"#Lowpromoted\n" 

        f"<b>Promoter :</b> {mention_html(user.id, user.first_name)}\n" 

        f"<b>User :</b> {mention_html(user_member.user.id, user_member.user.first_name)}" 

    ) 

  

    return log_message 

  

  

@connection_status 

@bot_admin 

@can_promote 

@user_admin 

@loggable 

def fullpromote(update: Update, context: CallbackContext) -> str: 

    bot = context.bot 

    args = context.args 

  

    message = update.effective_message 

    chat = update.effective_chat 

    user = update.effective_user 

  

    promoter = chat.get_member(user.id) 

  

    if ( 

        not (promoter.can_promote_members or promoter.status == "creator") 

        and user.id not in DRAGONS 

    ): 

        message.reply_text("• You don't have permissions to add new admins !") 

        return 

  

    user_id = extract_user(message, args) 

  

    if not user_id: 

        message.reply_text( 

            "• I don't know who's that user, never seen him in any of the chats where i am present !", 

        ) 

        return 

  

    try: 

        user_member = chat.get_member(user_id) 

    except: 

        return 

  

    if user_member.status in ("administrator", "creator"): 

        message.reply_text("• According to me that user is already an admin here !") 

        return 

  

    if user_id == bot.id: 

        message.reply_text( 

            "• I can't promote myself, my owner didn't told me to do so." 

        ) 

        return 

  

    # set same perms as bot - bot can't assign higher perms than itself! 

    bot_member = chat.get_member(bot.id) 

  

    try: 

        bot.promoteChatMember( 

            chat.id, 

            user_id, 

            can_change_info=bot_member.can_change_info, 

            can_post_messages=bot_member.can_post_messages, 

            can_edit_messages=bot_member.can_edit_messages, 

            can_delete_messages=bot_member.can_delete_messages, 

            can_invite_users=bot_member.can_invite_users, 

            can_promote_members=bot_member.can_promote_members, 

            can_restrict_members=bot_member.can_restrict_members, 

            can_pin_messages=bot_member.can_pin_messages, 

            can_manage_voice_chats=bot_member.can_manage_voice_chats, 

        ) 

    except BadRequest as err: 

        if err.message == "User_not_mutual_contact": 

            message.reply_text("• As i can see that user is not present here.") 

        else: 

            message.reply_text( 

                "• something went wrong, maybe someone promoted that user before me." 

            ) 

        return 

  

    bot.sendMessage( 

        chat.id, 

        f"• fullpromoting a user in <b>{chat.title}</b>\n\n<b>User : {mention_html(user_member.user.id, user_member.user.first_name)}</b>\n<b>Promoter : {mention_html(user.id, user.first_name)}</b>", 

        parse_mode=ParseMode.HTML, 

    ) 

  

    log_message = ( 

        f"<b>{html.escape(chat.title)}:</b>\n" 

        f"#fullpromoted\n" 

        f"<b>Promoter :</b> {mention_html(user.id, user.first_name)}\n" 

        f"<b>User :</b> {mention_html(user_member.user.id, user_member.user.first_name)}" 

    ) 

  

    return log_message 

  

  

@connection_status 

@bot_admin 

@can_promote 

@user_admin 

@loggable 

def demote(update: Update, context: CallbackContext) -> str: 

    bot = context.bot 

    args = context.args 

  

    chat = update.effective_chat 

    message = update.effective_message 

    user = update.effective_user 

  

    user_id = extract_user(message, args) 

    if not user_id: 

        message.reply_text( 

            "• I don't know who's that user, never seen him in any of the chats where i am present !", 

        ) 

        return 

  

    try: 

        user_member = chat.get_member(user_id) 

    except: 

        return 

  

    if user_member.status == "creator": 

        message.reply_text( 

            "• That user is owner of the chat and i don't want to put myself in danger." 

        ) 

        return 

  

    if not user_member.status == "administrator": 

        message.reply_text("• According to me that user is not an admin here !") 

        return 

  

    if user_id == bot.id: 

        message.reply_text("• I can't demote myself, but if you want i can leave.") 

        return 

  

    try: 

        bot.promoteChatMember( 

            chat.id, 

            user_id, 

            can_change_info=False, 

            can_post_messages=False, 

            can_edit_messages=False, 

            can_delete_messages=False, 

            can_invite_users=False, 

            can_restrict_members=False, 

            can_pin_messages=False, 

            can_promote_members=False, 

            can_manage_voice_chats=False, 

        ) 

  

        bot.sendMessage( 

            chat.id, 

            f"• successfully demoted an admin in <b>{chat.title}</b>\n\nDemoted : <b>{mention_html(user_member.user.id, user_member.user.first_name)}</b>\nDemoter : {mention_html(user.id, user.first_name)}", 

            parse_mode=ParseMode.HTML, 

        ) 

  

        log_message = ( 

            f"<b>{html.escape(chat.title)}:</b>\n" 

            f"#Demoted\n" 

            f"<b>Demoter :</b> {mention_html(user.id, user.first_name)}\n" 

            f"<b>Demoted :</b> {mention_html(user_member.user.id, user_member.user.first_name)}" 

        ) 

  

        return log_message 

    except BadRequest: 

        message.reply_text( 

            "• failed to demote maybe i'm not an admin or maybe someone else promoted that" 

            " User !", 

        ) 

        return 

  

  

@user_admin 

def refresh_admin(update, _): 

    try: 

        ADMIN_CACHE.pop(update.effective_chat.id) 

    except KeyError: 

        pass 

  


        send_message( 

            update.effective_message, 

            "✅ Bot restarted \n✅ Admin list updated", 

        ) 

  

  

@connection_status 

@bot_admin 

@can_promote 

@user_admin 

def set_title(update: Update, context: CallbackContext): 

    bot = context.bot 

    args = context.args 

  

    chat = update.effective_chat 

    message = update.effective_message 

  

    user_id, title = extract_user_and_text(message, args) 

    try: 

        user_member = chat.get_member(user_id) 

    except: 

        return 

  

    if not user_id: 

        message.reply_text( 

            "• I don't know who's that user, never seen him in any of the chats where i am present !", 

        ) 

        return 

  

    if user_member.status == "creator": 

        message.reply_text( 

            "• That user is owner of the chat and i don't want to put myself in danger.", 

        ) 

        return 

  

    if user_member.status != "administrator": 

        message.reply_text( 

            "• I cAN oNLY sET TITLE foR ADMINs !", 

        ) 

        return 

  

    if user_id == bot.id: 

        message.reply_text( 

            "• I can't set title for myself, my owner didn't told me to do so.", 

        ) 

        return 

  

    if not title: 

        message.reply_text( 

            "• You think that setting blank title will change something ?" 

        ) 

        return 

  

    if len(title) > 16: 

        message.reply_text( 

            "• The title length is longer than 16 words or characters so truncating it to 16 words.", 

        ) 

  

    try: 

        bot.setChatAdministratorCustomTitle(chat.id, user_id, title) 

    except BadRequest: 

        message.reply_text( 

            "• Maybe that user is not promoted by me or maybe you sent something that can't be set as title." 

        ) 

        return 

  

    bot.sendMessage( 

        chat.id, 

        f"• successfully set title for <code>{user_member.user.first_name or user_id}</code> " 

        f"To <code>{html.escape(title[:16])}</code>!", 

        parse_mode=ParseMode.HTML, 

    ) 

  

  

@bot_admin 

@can_pin 

@user_admin 

@loggable 

def pin(update: Update, context: CallbackContext) -> str: 

    bot, args = context.bot, context.args 

    user = update.effective_user 

    chat = update.effective_chat 

    msg = update.effective_message 

    msg_id = msg.reply_to_message.message_id if msg.reply_to_message else msg.message_id 

  

    if msg.chat.username: 

        # If chat has a username, use this format 

        link_chat_id = msg.chat.username 

        message_link = f"https://t.me/{link_chat_id}/{msg_id}" 

    elif (str(msg.chat.id)).startswith("-100"): 

        # If chat does not have a username, use this 

        link_chat_id = (str(msg.chat.id)).replace("-100", "") 

        message_link = f"https://t.me/c/{link_chat_id}/{msg_id}" 

  

    is_group = chat.type not in ("private", "channel") 

    prev_message = update.effective_message.reply_to_message 

  

    if prev_message is None: 

        msg.reply_text("• Reply to a message to pin it !") 

        return 

  

    is_silent = True 

    if len(args) >= 1: 

        is_silent = ( 

            args[0].lower() != "notify" 

            or args[0].lower() == "loud" 

            or args[0].lower() == "violent" 

        ) 

  

    if prev_message and is_group: 

        try: 

            bot.pinChatMessage( 

                chat.id, prev_message.message_id, disable_notification=is_silent 

            ) 

            msg.reply_text( 

                f"• successfully pinned that message.\nclick on the button below to see the message.", 

                reply_markup=InlineKeyboardMarkup( 

                    [[InlineKeyboardButton("Message", url=f"{message_link}")]] 

                ), 

                parse_mode=ParseMode.HTML, 

                disable_web_page_preview=True, 

            ) 

        except BadRequest as excp: 

            if excp.message != "Chat_not_modified": 

                raise 

  

        log_message = ( 

            f"<b>{html.escape(chat.title)}:</b>\n" 

            f"Pinned-a-message\n" 

            f"<b>PInned By :</b> {mention_html(user.id, html.escape(user.first_name))}" 

        ) 

  

        return log_message 

  

  

@bot_admin 

@can_pin 

@user_admin 

@loggable 

def unpin(update: Update, context: CallbackContext): 

    chat = update.effective_chat 

    user = update.effective_user 

    msg = update.effective_message 

    msg_id = msg.reply_to_message.message_id if msg.reply_to_message else msg.message_id 

    unpinner = chat.get_member(user.id) 

  

    if ( 

        not (unpinner.can_pin_messages or unpinner.status == "creator") 

        and user.id not in DRAGONS 

    ): 

        message.reply_text( 

            "• You don't have permissions to pin/unpin messages in this chat !" 

        ) 

        return 

  

    if msg.chat.username: 

        # If chat has a username, use this format 

        link_chat_id = msg.chat.username 

        message_link = f"https://t.me/{link_chat_id}/{msg_id}" 

    elif (str(msg.chat.id)).startswith("-100"): 

        # If chat does not have a username, use this 

        link_chat_id = (str(msg.chat.id)).replace("-100", "") 

        message_link = f"https://t.me/c/{link_chat_id}/{msg_id}" 

  

    is_group = chat.type not in ("private", "channel") 

    prev_message = update.effective_message.reply_to_message 

  

    if prev_message and is_group: 

        try: 

            context.bot.unpinChatMessage(chat.id, prev_message.message_id) 

            msg.reply_text( 

                f"• successfully unpinned <a href='{message_link}'> this pinned message</a>.", 

                parse_mode=ParseMode.HTML, 

                disable_web_page_preview=True, 

            ) 

        except BadRequest as excp: 

            if excp.message != "Chat_not_modified": 

                raise 

  

    if not prev_message and is_group: 

        try: 

            context.bot.unpinChatMessage(chat.id) 

            msg.reply_text("• successfully unpinned the last pinned message.") 

        except BadRequest as excp: 

            if excp.message == "Message to unpin not found": 

                msg.reply_text( 

                    "• I can't unpin that message, maybe that message is too old or maybe someone already unpinned it." 

                ) 

            else: 

                raise 

  

    log_message = ( 

        f"<b>{html.escape(chat.title)}:</b>\n" 

        f"Unpinned-a-message\n" 

        f"<b>Unpinned by :</b> {mention_html(user.id, html.escape(user.first_name))}" 

    ) 

  

    return log_message 

  

  

@bot_admin 

def pinned(update: Update, context: CallbackContext) -> str: 

    bot = context.bot 

    msg = update.effective_message 

    msg_id = ( 

        update.effective_message.reply_to_message.message_id 

        if update.effective_message.reply_to_message 

        else update.effective_message.message_id 

    ) 

  

    chat = bot.getChat(chat_id=msg.chat.id) 

    if chat.pinned_message: 

        pinned_id = chat.pinned_message.message_id 

        if msg.chat.username: 

            link_chat_id = msg.chat.username 

            message_link = f"https://t.me/{link_chat_id}/{pinned_id}" 

        elif (str(msg.chat.id)).startswith("-100"): 

            link_chat_id = (str(msg.chat.id)).replace("-100", "") 

            message_link = f"https://t.me/c/{link_chat_id}/{pinned_id}" 

  

        msg.reply_text( 

            f"pinned on {html.escape(chat.title)}.", 

            reply_to_message_id=msg_id, 

            parse_mode=ParseMode.HTML, 

            disable_web_page_preview=True, 

            reply_markup=InlineKeyboardMarkup( 

                [ 

                    [ 

                        InlineKeyboardButton( 

                            text="Message", 

                            url=f"https://t.me/{link_chat_id}/{pinned_id}", 

                        ) 

                    ] 

                ] 

            ), 

        ) 

  

    else: 

        msg.reply_text( 

            f"• There's no pinned message in <b>{html.escape(chat.title)}!</b>", 

            parse_mode=ParseMode.HTML, 

        ) 

  

  

@bot_admin 

@user_admin 

@connection_status 

def invite(update: Update, context: CallbackContext): 

    bot = context.bot 

    chat = update.effective_chat 

  

    if chat.username: 

        update.effective_message.reply_text(f"https://t.me/{chat.username}") 

    elif chat.type in [chat.SUPERGROUP, chat.CHANNEL]: 

        bot_member = chat.get_member(bot.id) 

        if bot_member.can_invite_users: 

            invitelink = bot.exportChatInviteLink(chat.id) 

            update.effective_message.reply_text(invitelink) 

        else: 

            update.effective_message.reply_text( 

                "• I don't have permissions to access invite links !", 

            ) 

    else: 

        update.effective_message.reply_text( 

            "• I can only give invite links for groups and channels !", 

        ) 

  

  

@connection_status 

def adminlist(update, context): 

    chat = update.effective_chat  # type: Optional[Chat] -> unused variable 

    user = update.effective_user  # type: Optional[User] 

    args = context.args  # -> unused variable 

    bot = context.bot 

  

    if update.effective_message.chat.type == "private": 

        send_message( 

            update.effective_message, 

            "• This command can only be used in group's not in pm.", 

        ) 

        return 

  

    update.effective_chat 

    chat_id = update.effective_chat.id 

    chat_name = update.effective_message.chat.title  # -> unused variable 

  

    try: 

        msg = update.effective_message.reply_text( 

            "• fetching admins list...", 

            parse_mode=ParseMode.HTML, 

        ) 

    except BadRequest: 

        msg = update.effective_message.reply_text( 

            "• fetching admins list...", 

            quote=False, 

            parse_mode=ParseMode.HTML, 

        ) 

  

    administrators = bot.getChatAdministrators(chat_id) 

    text = "Admins in <b>{}</b>:".format(html.escape(update.effective_chat.title)) 

  

    for admin in administrators: 

        user = admin.user 

        status = admin.status 

        custom_title = admin.custom_title 

  

        if user.first_name == "": 

            name = "Deleted account" 

        else: 

            name = "{}".format( 

                mention_html( 

                    user.id, 

                    html.escape(user.first_name + " " + (user.last_name or "")), 

                ), 

            ) 

  

        if user.is_bot: 

            administrators.remove(admin) 

            continue 

  

        # if user.username: 

        #    name = escape_markdown("@" + user.username) 

        if status == "creator": 

            text += "\n  Owner :" 

            text += "\n<code> • </code>{}\n".format(name) 

  

            if custom_title: 

                text += f"<code> ┗- {html.escape(custom_title)}</code>\n" 

  

    text += "\nAdmins :" 

  

    custom_admin_list = {} 

    normal_admin_list = [] 

  

    for admin in administrators: 

        user = admin.user 

        status = admin.status 

        custom_title = admin.custom_title 

  

        if user.first_name == "": 

            name = "Deleted account" 

        else: 

            name = "{}".format( 

                mention_html( 

                    user.id, 

                    html.escape(user.first_name + " " + (user.last_name or "")), 

                ), 

            ) 

        # if user.username: 

        #    name = escape_markdown("@" + user.username) 

        if status == "administrator": 

            if custom_title: 

                try: 

                    custom_admin_list[custom_title].append(name) 

                except KeyError: 

                    custom_admin_list.update({custom_title: [name]}) 

            else: 

                normal_admin_list.append(name) 

  

    for admin in normal_admin_list: 

        text += "\n<code> • </code>{}".format(admin) 

  

    for admin_group in custom_admin_list.copy(): 

        if len(custom_admin_list[admin_group]) == 1: 

            text += "\n<code> • </code>{} | <code>{}</code>".format( 

                custom_admin_list[admin_group][0], 

                html.escape(admin_group), 

            ) 

            custom_admin_list.pop(admin_group) 

  

    text += "\n" 

    for admin_group, value in custom_admin_list.items(): 

        text += "\n <code>{}</code>".format(admin_group) 

        for admin in value: 

            text += "\n<code> • </code>{}".format(admin) 

        text += "\n" 

  

    try: 

        msg.edit_text(text, parse_mode=ParseMode.HTML) 

    except BadRequest:  # if original message is deleted 

        return 

  

  

__help__ = """ 

*User Commands*: 

• /admins*:* list of admins in the chat 

• /pinned*:* to get the current pinned message. 

  

*The Following Commands are Admins only:*  

• /pin*:* silently pins the message replied to - add `'loud'` or `'notify'` to give notifs to users 

• /unpin*:* unpins the currently pinned message 

• /invitelink*:* gets invitelink 

• /promote*:* promotes the user replied to 

• /lowpromote*:* promotes the user replied to with half rights 

• /fullpromote*:* promotes the user replied to with full rights 

• /demote*:* demotes the user replied to 

• /title <title here>*:* sets a custom title for an admin that the bot promoted 

• /admincache*:* force refresh the admins list 

• /del*:* deletes the message you replied to 

• /purge*:* deletes all messages between this and the replied to message. 

• /purge <integer X>*:* deletes the replied message, and X messages following it if replied to a message. 

• /setgtitle <text>*:* set group title 

• /setgpic*:* reply to an image to set as group photo 

• /setdesc*:* Set group description 

• /setsticker*:* Set group sticker 

""" 

  

SET_DESC_HANDLER = CommandHandler("setdesc", set_desc, run_async=True) 

SET_STICKER_HANDLER = CommandHandler("setsticker", set_sticker, run_async=True) 

SETCHATPIC_HANDLER = CommandHandler("setgpic", setchatpic, run_async=True) 

RMCHATPIC_HANDLER = CommandHandler("delgpic", rmchatpic, run_async=True) 

SETCHAT_TITLE_HANDLER = CommandHandler("setgtitle", setchat_title, run_async=True) 

  

ADMINLIST_HANDLER = DisableAbleCommandHandler( 

    ["admins", "staff"], adminlist, run_async=True 

) 

  

PIN_HANDLER = CommandHandler("pin", pin, run_async=True) 

UNPIN_HANDLER = CommandHandler("unpin", unpin, run_async=True) 

PINNED_HANDLER = CommandHandler("pinned", pinned, run_async=True) 

  

INVITE_HANDLER = DisableAbleCommandHandler("invitelink", invite, run_async=True) 

  

PROMOTE_HANDLER = DisableAbleCommandHandler("promote", promote, run_async=True) 

FULLPROMOTE_HANDLER = DisableAbleCommandHandler( 

    "fullpromote", fullpromote, run_async=True 

) 

LOW_PROMOTE_HANDLER = DisableAbleCommandHandler( 

    "lowpromote", lowpromote, run_async=True 

) 

DEMOTE_HANDLER = DisableAbleCommandHandler("demote", demote, run_async=True) 

  

SET_TITLE_HANDLER = CommandHandler("title", set_title, run_async=True) 

ADMIN_REFRESH_HANDLER = CommandHandler( 

    ["admincache", "reload", "refresh"], 

    refresh_admin, 

    run_async=True, 

) 

  

dispatcher.add_handler(SET_DESC_HANDLER) 

dispatcher.add_handler(SET_STICKER_HANDLER) 

dispatcher.add_handler(SETCHATPIC_HANDLER) 

dispatcher.add_handler(RMCHATPIC_HANDLER) 

dispatcher.add_handler(SETCHAT_TITLE_HANDLER) 

dispatcher.add_handler(ADMINLIST_HANDLER) 

dispatcher.add_handler(PIN_HANDLER) 

dispatcher.add_handler(UNPIN_HANDLER) 

dispatcher.add_handler(PINNED_HANDLER) 

dispatcher.add_handler(INVITE_HANDLER) 

dispatcher.add_handler(PROMOTE_HANDLER) 

dispatcher.add_handler(FULLPROMOTE_HANDLER) 

dispatcher.add_handler(LOW_PROMOTE_HANDLER) 

dispatcher.add_handler(DEMOTE_HANDLER) 

dispatcher.add_handler(SET_TITLE_HANDLER) 

dispatcher.add_handler(ADMIN_REFRESH_HANDLER) 

  

__mod_name__ = "Admin" 

__command_list__ = [ 

    "setdesc" "setsticker" "setgpic" "delgpic" "setgtitle" "adminlist", 

    "admins", 

    "invitelink", 

    "promote", 

    "fullpromote", 

    "lowpromote", 

    "demote", 

    "admincache", 

] 

__handlers__ = [ 

    SET_DESC_HANDLER, 

    SET_STICKER_HANDLER, 

    SETCHATPIC_HANDLER, 

    RMCHATPIC_HANDLER, 

    SETCHAT_TITLE_HANDLER, 

    ADMINLIST_HANDLER, 

    PIN_HANDLER, 

    UNPIN_HANDLER, 

    PINNED_HANDLER, 

    INVITE_HANDLER, 

    PROMOTE_HANDLER, 

    FULLPROMOTE_HANDLER, 

    LOW_PROMOTE_HANDLER, 

    DEMOTE_HANDLER, 

    SET_TITLE_HANDLER, 

    ADMIN_REFRESH_HANDLER, 

] 

  

from Exon.modules.language import gs  

  

   

  

   

  

def get_help(chat):  

  

    return gs(chat, "admin_help") 
