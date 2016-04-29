#! usr/bin/python
#  -_-  coding:utf-8 -_-

'''
@author          sugarguo

@email           sugarguo@live.com

@date            2016年04月15日

@version         v1.0.0 

@copyright       Sugarguo

File             main/views.py

'''


import os
import json
import time
import random 
import Image, ImageDraw, ImageFont, ImageFilter 
import StringIO

from datetime import datetime, date, timedelta
from flask import render_template, session, redirect, url_for, request, make_response, flash
from flask.ext.login import login_user, login_required, logout_user, current_user

from . import main
from .. import db
from ..models import User



#map:将str函数作用于后面序列的每一个元素
numbers = ''.join(map(str, range(10)))
chars = ''.join((numbers))

authcode = ""

 
def create_validate_code(size=(120, 30), 
                         chars=chars, 
                         mode="RGB", 
                         bg_color=(255, 255, 255), 
                         fg_color=(255, 0, 0), 
                         font_size=18,
                         font_type="MSYHMONO.ttf",
                         length=4, 
                         draw_points=True, 
                         point_chance = 2): 
    '''''
    size: 图片的大小，格式（宽，高），默认为(120, 30)
    chars: 允许的字符集合，格式字符串
    mode: 图片模式，默认为RGB
    bg_color: 背景颜色，默认为白色
    fg_color: 前景色，验证码字符颜色
    font_size: 验证码字体大小
    font_type: 验证码字体，默认为 Monaco.ttf
    length: 验证码字符个数
    draw_points: 是否画干扰点
    point_chance: 干扰点出现的概率，大小范围[0, 50]
    ''' 
 
    width, height = size 
    img = Image.new(mode, size, bg_color) # 创建图形 
    draw = ImageDraw.Draw(img) # 创建画笔 
 
    def get_chars(): 
        '''''生成给定长度的字符串，返回列表格式''' 
        return random.sample(chars, length) 
 
    def create_points(): 
        '''''绘制干扰点''' 
        chance = min(50, max(0, int(point_chance))) # 大小限制在[0, 50] 
 
        for w in xrange(width): 
            for h in xrange(height): 
                tmp = random.randint(0, 50) 
                if tmp > 50 - chance: 
                    draw.point((w, h), fill=(0, 0, 0)) 
 
    def create_strs(): 
        '''''绘制验证码字符''' 
        c_chars = get_chars() 
        strs = '%s' % ''.join(c_chars) 
 
        font = ImageFont.truetype(font_type, font_size) 
        font_width, font_height = font.getsize(strs) 
 
        draw.text(((width - font_width) / 3, (height - font_height) / 4), 
                    strs, font=font, fill=fg_color) 
 
        return strs 
 
    if draw_points: 
        create_points() 
    strs = create_strs() 
 
    # 图形扭曲参数 
    params = [1 - float(random.randint(1, 2)) / 100, 
              0, 
              0, 
              0, 
              1 - float(random.randint(1, 10)) / 100, 
              float(random.randint(1, 2)) / 500, 
              0.001, 
              float(random.randint(1, 2)) / 500 
              ] 
    img = img.transform(size, Image.PERSPECTIVE, params) # 创建扭曲 
 
    img = img.filter(ImageFilter.EDGE_ENHANCE_MORE) # 滤镜，边界加强（阈值更大） 
 
    return img,strs 


def site_get():
    meminfo = {}
    with open('/proc/meminfo') as f:
        for line in f:
            meminfo[line.split(':')[0]] = line.split(':')[1].strip()
    pids = []
    for subdir in os.listdir('/proc'):
        if subdir.isdigit():
            pids.append(subdir)
    site_info = {}
    site_info['site_name'] = 'Sugarguo_Flask_Blog'
    site_info['site_domain'] = 'http://www.sugarguo.com/'
    site_info['site_email'] = 'sugarguo@live.com'
        
    site_info['memuse'] = int(meminfo['MemTotal'][:-3]) - int(meminfo['MemFree'][:-3])
    site_info['pids'] = len(pids)
    return site_info


@main.route('/')
def index():
    site_info = site_get()
    return render_template('index.html', **locals())


@main.route('/login', methods = ['GET', 'POST'])
def login():
    site_info = site_get()
    session.permanent = True
    if request.method == 'POST':
        print session['code_text']
        username=request.form.get('username')
        user = User.query.filter_by(username=username).first()
        if user is not None and user.verify_password(password = request.form.get('password')) and \
            session['code_text'] == request.form.get('authcode'):
            login_user(user, request.form.get('remember_me'))
            return redirect(url_for('main.index'))
        flash(u'用户名或密码错误，请重试！')
    return render_template('login.html', **locals())


@main.route('/logout')
@login_required
def logout():
    site_info = site_get()
    logout_user()
    flash(u'你已经退出系统！')
    return redirect(url_for('main.index'))
    
    
    
@main.route('/get_code')
def get_code():
    main.permanent_session_lifetime = timedelta(minutes=1)
    code_img,code_text = create_validate_code()
    session['code_text'] = code_text
    buf = StringIO.StringIO() 
    code_img.save(buf,'JPEG',quality=70) 
 
    buf_str = buf.getvalue() 
    response = make_response(buf_str)  
    response.headers['Content-Type'] = 'image/jpeg'  
    return response
