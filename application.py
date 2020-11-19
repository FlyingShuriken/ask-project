from flask import *
import csv

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check',methods= ["GET","POST"])
def check():
    return render_template('check.html')

@app.route('/search',methods= ["GET","POST"])
def search():
    result = []
    total = 0
    name = str(request.form.get("name"))
    classes = str(request.form.get("class"))
    with open(f'csv/{classes[0]}.csv','r') as database:
        db = csv.DictReader(database)
        for row in db:
            if row['name'] == name.upper() and row['class'] == classes.upper():
                result.append(row)
    for a in result:
        now = int(a['marks'])
        total += now
    if total >= 20 and total <=39:
        result.append({'datetime':'','name':'','class':'','marks':'TOTAL:','reason':'TINDAKAN:'})
        result.append({'datetime':'','name':'','class':'','marks':total,'reason':'AMARAN PERTAMA'})
    elif total >= 40 and total <= 59:
        result.append({'datetime':'','name':'','class':'','marks':'Total:','reason':'TINDAKAN'})
        result.append({'datetime':'','name':'','class':'','marks':total,'reason':'AMARAN KEDUA'})
    elif total >= 60 and total <= 79:
        result.append({'datetime':'','name':'','class':'','marks':'Total:','reason':'TINDAKAN'})
        result.append({'datetime':'','name':'','class':'','marks':total,'reason':'AMARAN KETIGA'})
    elif total >=80:
        result.append({'datetime':'','name':'','class':'','marks':'Total:','reason':'TINDAKAN'})
        result.append({'datetime':'','name':'','class':'','marks':total,'reason':'KAUNSELING/PERJANJIAN TERAKHIR'})
    else:
        result.append({'datetime':'','name':'','class':'','marks':'TOTAL:','reason':'TINDAKAN:'})
        result.append({'datetime':'','name':'','class':'','marks':total,'reason':'TIDAK ADA TINDAKAN'})
    return render_template('search.html',results=result)

@app.route('/all',methods= ["GET","POST"])
def all():
    result = []
    form = str(request.form.get("form","1"))
    classes = str(request.form.get("class"))
    with open(f'csv/{form}.csv','r') as database:
        db = csv.DictReader(database)
        t = f"{form}{classes.upper()}"
        for row in db:
            if row['class'] == t:
                result.append(row)
    return render_template('all.html',results=result)

@app.route('/record',methods= ["GET","POST"])
def record():
    date = request.form.get("date")
    time = request.form.get("time")
    name = str(request.form.get("name"))
    classes = str(request.form.get("class",''))
    marks = request.form.get("marks")
    reason = str(request.form.get("reason"))
    datetime = f"{date} {time}"
    if classes != '':
        with open(f'csv/{classes[0]}.csv','a+',newline='\n') as database:
            w = csv.writer(database)
            w.writerow([datetime,name.upper(),classes.upper(),marks,reason])
    return render_template('record.html')

if __name__ == '__main__':
    print("Sila buka browser dan melayari laman (http://localhost:5879)")
    app.run(debug=True,host='0.0.0.0', port=5879)