from kilakochen.user import bp    
from flask import render_template
from flask_login import login_required

from kilakochen.models import User

@bp.route('/overview', methods=['GET', 'POST'])
@login_required
def overview():
    all_user = User.query.all()
    return render_template(
        'user/overview.html',
        data=all_user
    )

