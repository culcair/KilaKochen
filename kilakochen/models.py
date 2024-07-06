from typing import Optional

from sqlalchemy import Date, Double, ForeignKey, Index, Text, text
from sqlalchemy.dialects.mysql import INTEGER, MEDIUMTEXT, TEXT
from sqlalchemy.orm import Mapped, mapped_column, relationship
import datetime
import decimal

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

from werkzeug.security import generate_password_hash, check_password_hash

from kilakochen import login, db



@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))

   
class User(db.Model, UserMixin):
    __tablename__ = 'kila_jakobi_anwender'

    ID: Mapped[int] = mapped_column(INTEGER(11), primary_key=True)
    name: Mapped[str] = mapped_column(Text)
    vorname: Mapped[str] = mapped_column(Text)
    user: Mapped[str] = mapped_column(Text)
    password: Mapped[str] = mapped_column(Text)
    mail: Mapped[str] = mapped_column(Text)
    level: Mapped[int] = mapped_column(INTEGER(11))
    active: Mapped[int] = mapped_column(INTEGER(11))

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password,password)


class Essensplan(db.Model):
    __tablename__ = 'kila_jakobi_essensplan'

    wplan_id: Mapped[int] = mapped_column(INTEGER(11), primary_key=True)
    wplan_kw: Mapped[int] = mapped_column(INTEGER(11))
    wplan_jahr: Mapped[int] = mapped_column(INTEGER(11))
    wplan_wtag: Mapped[int] = mapped_column(INTEGER(11))
    wplan_hgericht: Mapped[Optional[int]] = mapped_column(INTEGER(11))
    wplan_beilage: Mapped[Optional[int]] = mapped_column(INTEGER(11))
    wplan_dessert: Mapped[Optional[int]] = mapped_column(INTEGER(11))
    wplan_ausfall: Mapped[Optional[str]] = mapped_column(Text)
    wplan_note: Mapped[Optional[str]] = mapped_column(Text)


class Mengenangabe(db.Model):
    __tablename__ = 'kila_jakobi_mengenangabe'
    __table_args__ = (
        Index('angaben_name', 'angaben_name', unique=True),
        Index('angaben_name_2', 'angaben_name')
    )

    angaben_id: Mapped[int] = mapped_column(INTEGER(11), primary_key=True)
    angaben_name: Mapped[str] = mapped_column(TEXT)
    angaben_abkz: Mapped[str] = mapped_column(TEXT)


class Rezepte(db.Model):
    __tablename__ = 'kila_jakobi_rezepte'
    __table_args__ = (
        Index('rezept_name', 'rezept_name', unique=True),
    )

    rezept_id: Mapped[int] = mapped_column(INTEGER(11), primary_key=True)
    rezept_name: Mapped[str] = mapped_column(TEXT)
    rezept_desc: Mapped[str] = mapped_column(TEXT)
    rezept_cat: Mapped[str] = mapped_column(TEXT)
    hgericht: Mapped[int] = mapped_column(INTEGER(11), server_default=text('0'))
    beilage: Mapped[int] = mapped_column(INTEGER(11), server_default=text('0'))
    dessert: Mapped[int] = mapped_column(INTEGER(11), server_default=text('0'))
    rezept_auth: Mapped[str] = mapped_column(TEXT)
    rezept_date: Mapped[datetime.date] = mapped_column(Date)
    rezept_text: Mapped[str] = mapped_column(MEDIUMTEXT)


class Zutaten(db.Model):
    __tablename__ = 'kila_jakobi_zutaten'
    __table_args__ = (
        Index('I_Z_NAME', 'zutat_name', unique=True),
    )

    zutat_id: Mapped[int] = mapped_column(INTEGER(11), primary_key=True)

    allergen_ei: Mapped[int] = mapped_column(INTEGER(11), server_default=text('0'))
    allergen_en: Mapped[int] = mapped_column(INTEGER(11), server_default=text('0'))
    allergen_fi: Mapped[int] = mapped_column(INTEGER(11), server_default=text('0'))
    allergen_gl: Mapped[int] = mapped_column(INTEGER(11), server_default=text('0'))
    allergen_kr: Mapped[int] = mapped_column(INTEGER(11), server_default=text('0'))
    allergen_lu: Mapped[int] = mapped_column(INTEGER(11), server_default=text('0'))
    allergen_mi: Mapped[int] = mapped_column(INTEGER(11), server_default=text('0'))
    allergen_s: Mapped[int] = mapped_column(INTEGER(11), server_default=text('0'))
    allergen_sw: Mapped[int] = mapped_column(INTEGER(11), server_default=text('0'))
    allergen_sl: Mapped[int] = mapped_column(INTEGER(11), server_default=text('0'))
    allergen_sf: Mapped[int] = mapped_column(INTEGER(11), server_default=text('0'))
    allergen_se: Mapped[int] = mapped_column(INTEGER(11), server_default=text('0'))
    allergen_so: Mapped[int] = mapped_column(INTEGER(11), server_default=text('0'))
    allergen_wt: Mapped[int] = mapped_column(INTEGER(11), server_default=text('0'))
    zusatz_farbst: Mapped[int] = mapped_column(INTEGER(11), server_default=text('0'))
    zusatz_konserv: Mapped[int] = mapped_column(INTEGER(11), server_default=text('0'))
    zusatz_antioxi: Mapped[int] = mapped_column(INTEGER(11), server_default=text('0'))
    zusatz_geschmv: Mapped[int] = mapped_column(INTEGER(11), server_default=text('0'))
    zusatz_gschwefel: Mapped[int] = mapped_column(INTEGER(11), server_default=text('0'))
    zusatz_gschwarz: Mapped[int] = mapped_column(INTEGER(11), server_default=text('0'))
    zusatz_phosphat: Mapped[int] = mapped_column(INTEGER(11), server_default=text('0'))
    zusatz_milcheiw: Mapped[int] = mapped_column(INTEGER(11), server_default=text('0'))
    zusatz_koffein: Mapped[int] = mapped_column(INTEGER(11), server_default=text('0'))
    zusatz_chinin: Mapped[int] = mapped_column(INTEGER(11), server_default=text('0'))
    zusatz_suessung: Mapped[int] = mapped_column(INTEGER(11), server_default=text('0'))
    zusatz_phenylan: Mapped[int] = mapped_column(INTEGER(11), server_default=text('0'))
    zusatz_gwachs: Mapped[int] = mapped_column(INTEGER(11), server_default=text('0'))
    zusatz_taurin: Mapped[int] = mapped_column(INTEGER(11), server_default=text('0'))
    zutat_name: Mapped[Optional[str]] = mapped_column(TEXT)
    zutat_quelle: Mapped[Optional[str]] = mapped_column(Text)
    zutat_auth: Mapped[Optional[str]] = mapped_column(Text)
    zutat_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    zutat_gruppe: Mapped[int] = mapped_column(ForeignKey("kila_jakobi_zutatengruppe.zutatengruppe_id"))
    zutaten_gruppe: Mapped["Zutatengruppe"] = relationship("Zutatengruppe", back_populates="zutaten")


class ZutatenProRezept(db.Model):
    __tablename__ = 'kila_jakobi_zutaten_pro_rezept'

    ID: Mapped[int] = mapped_column(INTEGER(11), primary_key=True)
    Rezept_ID: Mapped[int] = mapped_column(INTEGER(11))
    Zutat_ID: Mapped[int] = mapped_column(INTEGER(11))
    Menge: Mapped[decimal.Decimal] = mapped_column(Double(asdecimal=False))
    Einheit: Mapped[int] = mapped_column(INTEGER(2))


class Zutatengruppe(db.Model):
    __tablename__ = 'kila_jakobi_zutatengruppe'

    zutatengruppe_id: Mapped[int] = mapped_column(INTEGER(11), primary_key=True)
    zutatengruppe_name: Mapped[str] = mapped_column(Text)
    zutaten: Mapped[list["Zutaten"]] = relationship("Zutaten", back_populates="zutaten_gruppe")