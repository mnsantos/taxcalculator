
# -*- coding: utf-8 -*-

# Simple Bot to reply to Telegram messages
# This program is dedicated to the public domain under the CC0 license.
"""
This Bot uses the Updater class to handle the bot.
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

from telegram import (ReplyKeyboardMarkup)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler, Job)

import logging
from currency_converter import CurrencyConverter
from calculator import Calculator
from state_saver import StateSaver
from params import Params
import datetime
from datetime import timedelta

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

YES_NO_KEYBOARD = [['Si', 'No']]
ESCRITURAS_KEYBOARD = [['Compraventa']]
MONEDAS_KEYBOARD = [['ARS', 'USD']]
FECHAS_KEYBOARD = [['Hoy', 'Mañana']]

CHECK_MONEDA, CHECK_PRECIO, CHECK_FECHA, CHECK_TIPO_ESCRITURA, CHECK_REEMPLAZO, CHECK_GANANCIAS, CHECK_PROPIEDAD, CHECK_VIR, CHECK_VF = range(9)
global data, ids, ratios, calculator, state_saver

def calcular(bot, update):
  chat_id = update.message.chat_id
  data[chat_id] = Params()
  update.message.reply_text('Hola, ¿tipo de escritura?', reply_markup=ReplyKeyboardMarkup(ESCRITURAS_KEYBOARD, one_time_keyboard=True))
  return CHECK_TIPO_ESCRITURA

def check_tipo_escritura(bot, update):
  logger.info("check_tipo_escritura")
  chat_id = update.message.chat_id
  answer = update.message.text
  data[chat_id].tipo = answer
  if answer == 'Compraventa':
    update.message.reply_text('Ingrese la fecha de la escritura (FORMATO: ddmmyyyy. Ejemplo: 24102017) o seleccione alguna opcion si corresponde', reply_markup=ReplyKeyboardMarkup(FECHAS_KEYBOARD, one_time_keyboard=True))
    return CHECK_FECHA
  else:
    update.message.reply_text('Tipo de escritura no reconocido. Por favor ingrese el tipo de escritura nuevamente.', reply_markup=ReplyKeyboardMarkup(ESCRITURAS_KEYBOARD, one_time_keyboard=True))
    return CHECK_TIPO_ESCRITURA

def check_fecha(bot, update):
  logger.info("check_fecha")
  chat_id = update.message.chat_id
  answer = update.message.text
  today = datetime.datetime.now()
  if ('Hoy' == answer):
    date = today.date()
  elif (u'Mañana' == answer):
    date = (today + timedelta(days=1)).date()
  else:
    date = datetime.datetime.strptime(answer, '%d%m%Y').date()
  update.message.reply_text('¿Precio?')
  data[chat_id].fecha = date
  return CHECK_PRECIO

def check_precio(bot, update):
  logger.info("check_precio")
  chat_id = update.message.chat_id
  answer = update.message.text
  data[chat_id].precio = float(answer)
  update.message.reply_text('¿En que moneda se encuentra?', reply_markup=ReplyKeyboardMarkup(MONEDAS_KEYBOARD, one_time_keyboard=True))
  return CHECK_MONEDA

def check_moneda(bot, update):
  logger.info("check_moneda")
  chat_id = update.message.chat_id
  answer = update.message.text
  data[chat_id].moneda = answer
  update.message.reply_text('¿El vendedor paga IG?', reply_markup=ReplyKeyboardMarkup(YES_NO_KEYBOARD, one_time_keyboard=True))
  return CHECK_GANANCIAS

def check_ganancias(bot, update):
  logger.info("check_ig")
  chat_id = update.message.chat_id
  answer = update.message.text
  if answer == 'Si':
    data[chat_id].ganancias = True
    update.message.reply_text('¿El comprador tiene otra propiedad en CABA?', reply_markup=ReplyKeyboardMarkup(YES_NO_KEYBOARD, one_time_keyboard=True))
    return CHECK_PROPIEDAD
  else:
    data[chat_id].iti = True
    update.message.reply_text('¿Tiene certificado de no retencion de ITI?', reply_markup=ReplyKeyboardMarkup(YES_NO_KEYBOARD, one_time_keyboard=True))
    return CHECK_REEMPLAZO

def check_reemplazo(bot, update):
  logger.info("check_reemplazo")
  chat_id = update.message.chat_id
  answer = update.message.text
  if answer == 'Si':
    data[chat_id].reemplazo = True
  update.message.reply_text('¿El comprador tiene otra propiedad en CABA?', reply_markup=ReplyKeyboardMarkup(YES_NO_KEYBOARD, one_time_keyboard=True))
  return CHECK_PROPIEDAD

def check_propiedad(bot, update):
  logger.info("check_propiedad")
  chat_id = update.message.chat_id
  answer = update.message.text
  if answer == 'Si':
    data[chat_id].otra_propiedad = True
  update.message.reply_text('Ingrese VF')
  return CHECK_VF

def check_vf(bot, update):
  logger.info("check vf")
  chat_id = update.message.chat_id
  answer = update.message.text
  data[chat_id].vf = float(answer)
  update.message.reply_text('Ingrese VIR')
  return CHECK_VIR

def check_vir(bot, update, job_queue):
  logger.info("check vir")
  chat_id = update.message.chat_id
  answer = update.message.text
  data[chat_id].vir = float(answer)
  params = data[chat_id]
  logger.info(data)
  if calculator.can_calculate(params):
    update.message.reply_text(calculator_message(params))
  else:
    schedule_job(params, chat_id, job_queue)
    update.message.reply_text("Su pedido no puede ser procesado en este momento ya que la fecha que ingreso es futura (" + str(params.fecha) + "). Se le enviara un mensaje el dia " + str(params.fecha + timedelta(days=-1)) + " a las 15:30hs con el pedido solicitado. Numero de referencia: " + str(params.id))
  return ConversationHandler.END

def error(bot, update, error):
  logger.warn('Update "%s" caused error "%s"' % (update, error))

def cancel(bot, update):
  user = update.message.from_user
  logger.info("User %s canceled the conversation." % user.first_name)
  update.message.reply_text('Chau!')
  return ConversationHandler.END

def generate_id():
  if not ids:
    id = 1
  else:
    id = max(ids) + 1
  ids.append(id)
  return id

def alarm(bot, job):
  logger.info(job.context)
  id = job.context.id
  ids.remove(id)
  bot.sendMessage(job.context.chat_id, text='Pedido ' + str(id) + ':\n' + calculator_message(params))

def calculator_message(params):
  try:
    return calculator.calculate(params)
  except Exception as e:
    logger.error(e)
    return e.message
  finally:
    logger.info(ratios)
    state_saver.save(data, ids, ratios)

def schedule_job(params, chat_id, job_queue):
  today = datetime.datetime.now()
  date = params.fecha
  currency_date = date.replace(day = date.day - 1)
  currency_date_dt = datetime.datetime(currency_date.year, currency_date.month, currency_date.day, 15, 30)
  seconds = (currency_date_dt - today).seconds
  logger.info("Programando pedido para dentro de " + str(seconds) + " segundos.")
  #seconds = 10
  id = generate_id()
  params.id = id
  params.chat_id = chat_id
  job = Job(alarm, seconds, repeat=False, context=params)
  job_queue.put(job)
  state_saver.save(data, ids, ratios)


def main():
  global data, ids, ratios, calculator, state_saver

  # Create the EventHandler and pass it your bot's token.
  updater = Updater("304421327:AAF6V6IJh3q60COrgapidTtmiQx5eNl79WI")
  state_saver = StateSaver()
  try:
    data, ids, ratios = state_saver.load()
    logger.info("Loading ids " + str(ids))
    logger.info("Loading data " + str(data))
    logger.info("Loading ratios " + str(ratios))
  except Exception as e:
    ids = []
    ratios = dict()
    data = dict()
    logger.info("Cannot load state from hard drive. Skipping...")

  currency_converter = CurrencyConverter(ratios)
  calculator = Calculator(currency_converter)
  # ratios[datetime.date(2017, 2, 22)] = 15.7
  # ratios[datetime.date(2017, 2, 21)] = 15.8
  # ratios[datetime.date(2017, 2, 20)] = 15.9
  # state_saver.save(data, ids, ratios)

  # Get the dispatcher to register handlers
  dp = updater.dispatcher

  conv_handler = ConversationHandler(
    entry_points=[CommandHandler('calcular', calcular)],

    states={
      CHECK_TIPO_ESCRITURA: [MessageHandler(Filters.text, check_tipo_escritura)],
      CHECK_FECHA: [MessageHandler(Filters.text, check_fecha)],
      CHECK_MONEDA: [RegexHandler('^(ARS|USD)$', check_moneda)],
      CHECK_PRECIO: [MessageHandler(Filters.text, check_precio)],
      CHECK_REEMPLAZO: [RegexHandler('^(Si|No)$', check_reemplazo)],
      CHECK_GANANCIAS: [RegexHandler('^(Si|No)$', check_ganancias)],
      CHECK_PROPIEDAD: [RegexHandler('^(Si|No)$', check_propiedad)],
      CHECK_VF: [MessageHandler(Filters.text, check_vf)],
      CHECK_VIR: [MessageHandler(Filters.text, check_vir, pass_job_queue=True)]
    },

    fallbacks=[CommandHandler('cancel', cancel)]
  )

  dp.add_handler(conv_handler)

  # log all errors
  dp.add_error_handler(error)

  # Start the Bot
  updater.start_polling()

  # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
  # SIGTERM or SIGABRT. This should be used most of the time, since
  # start_polling() is non-blocking and will stop the bot gracefully.
  updater.idle()


if __name__ == '__main__':
    main()
