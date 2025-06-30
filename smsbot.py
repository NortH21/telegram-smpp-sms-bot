# -*- coding: utf-8 -*-

import os
import re
import logging
import sys
import urllib3

sys.path.append('./lib')
import smpplib

logging.basicConfig(level='INFO')
logger = logging.getLogger(__name__)

logger.info('Started')

bot_token = os.environ.get('telegram_bot_token')
channel_id = os.environ.get('telegram_channel_id')

proxy = urllib3.PoolManager()

# Two parts, UCS2, SMS with UDH
# parts, encoding_flag, msg_type_flag = smpplib.gsm.make_parts(u'Привет мир!\n' * 10)

client = smpplib.client.Client(os.environ.get('smpp_goip_host'), os.environ.get('smpp_goip_port'))
sms_destination_num = os.environ.get('smpp_goip_sim_num')

def getPdu(pdu):
   russian_symbols_count = len(re.findall('[а-яё]', pdu.short_message.decode('utf-16be', errors='ignore'), re.I))
   if russian_symbols_count > 0:
      logger.info(pdu.short_message.decode('utf-16be', errors='ignore'))
      sms = pdu.short_message.decode('utf-16be', errors='ignore')
   else:
      logger.info(pdu.short_message.decode())
      sms = pdu.short_message.decode()
   source_addr = pdu.source_addr.decode()
   msg = "СМС от (%s): %s" % (source_addr, sms)
   logger.info(msg)
   proxy.request('POST', "https://api.telegram.org/bot" + bot_token + "/sendMessage",
                 fields={"chat_id": channel_id, "text": msg, "disable_web_page_preview": "true"}).read()

client.set_message_received_handler(getPdu)

client.connect()

client.bind_transceiver(system_id=os.environ.get('smpp_goip_system_id'), password=os.environ.get('smpp_goip_password'))

# Enters a loop, waiting for incoming PDUs
client.listen()
