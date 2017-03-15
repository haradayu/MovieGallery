# -*- encoding: utf-8 -*- 
from flask import Flask, render_template
import glob
import os
from decorator import requires_auth 

app = Flask(__name__)
app.config['DEBUG'] = True

def tree(path, layer):
    exist_movie = False
    output_string = u""
    files = sorted(glob.glob(path + '/*'))
    for file in files:                      # get dir or file path
        file_paths = file.split('/')       # get dir or file name
        # print '\t' * layer + file_paths.pop()
        if os.path.islink(file):
            continue
        if os.path.isdir(file):             # case dir 
            tmp_str, tmp_flag = tree(file, layer + 1)
            if tmp_flag == True and exist_movie == False:
                exist_movie = True
            if tmp_flag == True:
                output_string += u'<li><span class="dir"><font color="darkorange">%s</font></span>\n<ul>' % os.path.basename(file).decode('utf_8') 
                output_string += tmp_str
                output_string += u"</ul>\n</li>\n"
        else:
            if os.path.splitext(file)[-1] == ".mp4":
                output_string += u'<li><a href="javascript:void(0);" onclick="playVideo(\'%s\');">%s</a></li>\n' % (file.decode('utf_8'), os.path.basename(file).decode('utf_8')) 
                exist_movie = True
    return output_string, exist_movie

@app.before_request # <- 全てのviewで前処理を行うためのdecoratorを使った関数を用意
@requires_auth          #<- ここでBasic認証のdecoratorを使う
def before_request():
    pass

@app.route('/')
def index():
    output, flag = tree("static/workspace", 0)
    return render_template('index.html', tree ="<ul>\n%s\n</ul>" %output)

@app.route('/player.html')
def player():
    return render_template('player.html')

@app.route("/menu.html")
def menu():
    output, flag = tree("..", 0)
    # print output
    return render_template("tree.html", tree ="<ul>\n%s\n</ul>" %output)

if __name__ == "__main__":
    app.run(port = 3000,host='0.0.0.0')