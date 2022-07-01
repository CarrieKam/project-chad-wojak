from email.policy import default
import os
from typing import Any
from urllib import response
from flask import Flask, make_response, render_template, request, redirect, url_for
from dotenv import load_dotenv
from peewee import *
from datetime import datetime
from playhouse.shortcuts import model_to_dict

load_dotenv()
app = Flask(__name__)

if os.getenv("TESTING") == "true":
    print("Running in test mode...")
    mydb = SqliteDatabase("file:memory?mode=memory&cache=shared", uri=True)

else:
    mydb = MySQLDatabase(
        os.getenv("MYSQL_DATABASE"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        host=os.getenv("MYSQL_HOST"),
        port=3306,
    )
print(mydb)

# Create a Timeline post
class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.now)

    class Meta:
        database = mydb

mydb.connect()
mydb.create_tables([TimelinePost])

# Base content all pages need
# used by the "profile" section of the template
base_content = {
    'name': 'Carrie Kam',
    'position': 'Software Engineer Student',
    'url': os.getenv("URL"),
    'socials': [{
        'name': 'Github',
        'url': 'https://github.com/CarrieKam',
        'icon': './static/img/social/github.svg'
    }, {
        'name': 'LinkedIn',
        'url': 'https://www.linkedin.com/in/carrie-kam-1837b3193/',
        'icon': './static/img/social/linkedin.svg'
    },{
        'name':'Email',
        'url':'mailto:carriekam@protonmail.com',
        'icon':'./static/img/social/mail.png'
    }]
}

@app.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
    name = request.form.get('name')
    email = request.form.get('email')
    content = request.form.get('content')
    if content == "" or content is None:
        return "Invalid content", 400
    elif "@" not in email or email == "" or email is None:
        return "Invalid email", 400
    elif name is None or name == "":
        return "Invalid name", 400
    else:
        timeline_post = TimelinePost.create(name=name, email=email, content=content)
        return model_to_dict(timeline_post)
        
        

@app.route('/api/timeline_post', methods=['GET'])
def get_time_line_post():
    return {
        'timeline_posts' : [
            model_to_dict(p)
            for p in
            TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }

@app.route('/')
def index():
    # no extra content needed
    # title and active_tab handled by `handle_route`
    return handle_route('Home', 'index', base_content)

@app.route('/timeline')
def timeline():
        content = {
            **base_content,
            'timeline_posts' : [ #get the new timeline
                model_to_dict(p)
                for p in
                TimelinePost.select().order_by(TimelinePost.created_at.desc())
            ]
        }
        return handle_route('Timeline', 'timeline', content)

@app.route('/about')
def about():
    motif = {
        **base_content,
        'quote': 'Only one who devotes himself to a cause with his whole strength and soul can be a true master. For this reason mastery demands all of a person.',
        'author': 'Albert Einstein',
    }
    return handle_route('About', 'about', motif)

@app.route('/work')
def work():
    motif = {
        **base_content,
        'jobs': [{
            'name': 'Theoretical physicist',
            'location': 'Mars',
            'contact': '1 (202) 358-0001',
            'description' : 'They wanted someone with a degree in theoretical physics and I said I have a theoretical physic degree and they let me in.'
        },{
            'name': 'Computer programmer',
            'location': 'Memory Lane',
            'contact': '127.255.255.255',
            'description' : 'Today I walked down a street where many computer programmers live. The houses were numbered 64k, 128k, 256k, 512k and 1MB. For some reason it felt like a trip down memory lane.'
        }]
    }
    return handle_route('Work Experiences', 'work', motif)

@app.route('/education')
def education():
    motif = {
        **base_content,
        'educations': [{
            'school': 'MLH Fellowship',
            'degree': 'Production Engineering',
            'years': 'Summer 2022 - Present'
        },{
            'school': 'Polytechnique de Montreal',
            'degree': 'Bachelor of Software Engineering',
            'years': 'Winter 2021 - Present'
        },{
            'school': 'Polytechnique de Montreal',
            'degree': 'Bachelor in Electrical Engineering',
            'years': 'Winter 2020 - Fall 2020'
        },{
            'school': 'College Maisonneuve',
            'degree': 'DEC in Computer Science and Mathematics ',
            'years': 'Fall 2017 - Winter 2020'
        }]
    }
    return handle_route('Education', 'education', motif)


@app.route('/hobbies')
def hobbies():
    motif = {
        'title': 'Hobbies - Portfolio',
        'active_tab': 'hobbies',
        'hobbies': [
            {
                'name': 'Violin',
                'img': 'https://images.unsplash.com/photo-1460036521480-ff49c08c2781?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=873&q=80',
                'desc': "I've been playing playing ever since I started secondary school. "
                        "Every year we had to do two concerts. We also assisted to a contest where we won gold."
            },
            {
                'name': 'Gaming',
                'img': 'https://images.unsplash.com/photo-1537963447914-dbc04b81de27?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=812&q=80',
                'desc': "I like escape games, like Tiny Room Stories: Town Mystery. Time flies very fast when playing this kind of game while "
                        "there is nothing to do in the subway. I also like Genshin Impact for the wonderful landscape and game play"
            },
            {
                'name': 'Attending Hackathons',
                'img': 'https://images.unsplash.com/photo-1640163561346-7778a2edf353?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=2070&q=80',
                'desc': "I like to meet new people. While doing awesome projects, it also pushes me to learn more than in school curriculum. "
            },
            {
                'name': 'Baking',
                'img': 'https://images.unsplash.com/photo-1517686469429-8bdb88b9f907?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=870&q=80',
                'desc': "I feel like the moment I am baking, I don't think other stuff and can focus in one thing."
                        " I enjoy the moment while making it and try to make it better for the next time."
            }

        ],
        **base_content
    }
    return handle_route('Hobbies', 'hobbies', motif)


@app.route('/where_am_i')
def where_am_i():
    motif = {
        **base_content,
        'places': [{
            'name': 'Montreal',
            'description': 'I am currently living in Quebec, Canada',
            'coords': [45.5579564,-73.8703871]
        }, {
            'name': 'Vancouver',
            'description': 'I went there for a very short time when I was small',
            'coords': [49.2573967,-123.4040887]
        },{
            'name': 'Seattle',
            'description': 'The seat of King County, Washington',
            'coords': [47, -120]
        },{
            'name': 'Guayaquil',
            'description': 'I went there to see family and visited beaches',
            'coords': [-2.1524948,-80.1201895]
        },{
            'name': 'Shanghai',
            'description': 'I went there almost every summer (very humid and hot during summer)',
            'coords': [31.2231337,120.9162723]
        },{
            'name': 'GuangDong',
            'description': 'Go food and very fun',
            'coords': [22.7739896,111.2470326]
        },{
            'name': 'Suzhou',
            'description': 'A lot of old buildings',
            'coords': [31.3280439,120.3641069]
        }],
        **base_content
    }
    return handle_route('Where am I', 'where_am_i', motif)


def handle_route(name: str, id: str, motif):
    '''
    Handles routing logic for each page

    Args:
        name: Page name (Shows in the navbar)
        id: unique id for the page
        content: extra content to pass to the template
    '''
    motif = {
        **motif,
        'title': f'{name} - Portfolio',
        'active_tab': id,
    }

    # check prev_page cookie to see what animations we have to do
    prev_page = request.cookies.get('prev_page', None, type=str)
    print(f'prev_page for {id}: {prev_page}')
    if prev_page is None or prev_page == id:
        # This is an initial page load (user first navigates, or refreshes)
        # `initial` is used by the template to know to play the fadein animations
        motif = {
            **motif,
            'initial': True,
        }
    else:
        # This is not an initial page load, so set a slide animation for the content
        motif = {
            **motif,
            'initial': False,
            'content_slide_animation': get_animation(prev_page, id)
        }
    # set the prev_page cookie to the `id`, 
    # so the next link will know what page transition to do
    resp = make_response(render_template(f'{id}.html', **motif))
    resp.set_cookie('prev_page', id)
    return resp


# from the two pages, gets the animate.css animation to play
# either a `animate__slideInLeft` or `animate__slideInRight`
def get_animation(prev_page: str, curr_page: str) -> str:
    pages = {'index': 0, 'about': 1, 'work': 2, 'education': 3, 'hobbies': 4, 'where_am_i': 5, 'timeline':6}
    anim = 'slideInRight' if pages[prev_page] < pages[curr_page] else 'slideInLeft'
    return f'animate__{anim}'


@app.route("/set")
@app.route("/set/<theme>")
def set_theme(theme='light'):
    res = make_response(redirect(url_for(request.cookies.get('prev_page'))))
    res.set_cookie("theme", theme)
    return res


if __name__ == '__main__':
    app.run(debug=True)
