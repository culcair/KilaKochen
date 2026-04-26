from babel.dates import format_date as f_d
from jinja2 import pass_eval_context
from markupsafe import Markup
from flask import current_app
from kilakochen.main import bp


@bp.app_template_filter()
def format_date(given_date, locale="de", kl_format="medium"):
    current_app.logger.debug(f"format_date: {given_date}")
    return f_d(date=given_date, locale=locale, format=kl_format)


@bp.app_template_filter()
def return_day(given_date, locale="de"):
    return f_d(date=given_date, locale=locale, format="EEEE")


@pass_eval_context
@bp.app_template_filter()
def nl2br(eval_ctx, value):
    result = value.replace("\r\n", "</br>")
    return Markup(result) if eval_ctx.autoescape else result