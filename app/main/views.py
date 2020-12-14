from flask import render_template,request,redirect,url_for,abort
from app.models import *
from . import main
from .. import db,photos
from flask_login import login_required, current_user
import markdown2
from .forms import *
from .forms import UpdateProfile,OpinionForm,CommentForm
from ..request import getquote

@main.route('/')
def index():
    '''
    Index page
    return
    '''
    
    message= "Welcome to BLOG Application!!"
    title= 'BLOG-app!'

    quote =getquote()


    return render_template('index.html', message=message,title=title , quote= quote) 

   


@main.route('/user/<uname>')
@login_required

def profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)
    return render_template("profile/profile.html", user = user)


@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required

def update_profile(uname):

    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)
    form = UpdateProfile()
    if form.validate_on_submit():
        user.bio = form.bio.data
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('.profile',uname=user.username))
    return render_template('profile/update.html',form =form)

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required

def update_pic(uname):

    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))



@main.route('/comment/<id>')
@login_required

def comment(id):
    '''
    function to return the comments
    '''
    comm =Comments.get_comment(id)
    
    title = 'comments'
    return render_template('comments.html',comment = comm,title = title)

@main.route('/opinion/', methods = ['GET','POST'])
@login_required

def new_opinion():


    quote = getquote()

    form = OpinionForm()
    
    if form.validate_on_submit():
        # category = form.category.data
        opinion= form.opinion.data
        title=form.title.data
        # Updated pitchinstance
        new_opinion= Opinion(title=title,opinion= opinion,user_id=current_user.id)
        title='New opinion'
        new_opinion.save_opinion()
        
        return redirect(url_for('main.new_opinion'))
    return render_template('opinion.html',form= form , quote = quote)

@main.route('/new_comment/<int:opinion_id>', methods = ['GET', 'POST'])
@login_required
def new_comment(opinion_id):

    opinion = Opinion.query.filter_by(id = opinion_id).first()
    form = CommentForm()
    if form.validate_on_submit():
        comment = form.comment.data
        new_comment = Comments(comment=comment,user_id=current_user.id, opinion_id=opinion_id)
        new_comment.save_comment()
        return redirect(url_for('main.index'))

    title='New opinion'
    return render_template('new_comment.html',title=title,comment_form = form,opinion_id=opinion_id)

# @main.route('/category/<cate>')

# def category(cate):
#     '''
#     function to return the pitches by category
#     '''
#     category = Pitches.get_pitches(cate)
#     title = f'{cate}'
#     return render_template('categories.html',title = title, category = category)