import sqlite3
#from flask import Flask
#from flask import render_template
#from flask import url_for
#from flask import redirect
from flask import *
from collections import OrderedDict

app = Flask(__name__)

## SQLITE DB


def get_1000_Genes():
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute("SELECT * FROM Genes LIMIT 1000")
    data = c.fetchall()
    conn.close()
    return data

def get_gene_by_ID(id):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    id = "'" + str(id) + "'"
    c.execute("SELECT * FROM GENES WHERE Ensembl_Gene_ID= %s" % id)
    data = c.fetchall()
    conn.close()
    return data

def get_transcript_list(id):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    id = "'" + str(id) + "'"
    c.execute("SELECT Ensembl_Transcript_ID, Transcript_Start, Transcript_End FROM Transcripts WHERE Ensembl_Gene_ID=%s" % id)
    data = c.fetchall()
    conn.close()
    return data


def build_gene_dict(gene_tuple):
    gene = OrderedDict()
    gene["Ensembl_Gene_ID"] = gene_tuple[0]
    gene["Chromosome_Name"] = gene_tuple[1]
    gene["Band"] = gene_tuple[2]
    gene["Strand"] = gene_tuple[3]
    gene["Gene_Start"] = gene_tuple[4]
    gene["Gene_End"] = gene_tuple[5]
    gene["Associated_Gene_Name"] = gene_tuple[6]
    gene["Transcript_Count"] = gene_tuple[7]
    return gene

def delete_gene(id):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    id = "'" + str(id) + "'"
    c.execute("DELETE FROM Genes WHERE Ensembl_Gene_ID=%s" % id)
    conn.commit()

@app.route("/")
def root():
    return render_template("./root.html", view = url_for("view"))

@app.route("/Genes/")
def view():
    results = get_1000_Genes()
    gene_list = []
    for gene_tuple in results:
        gene_ID = gene_tuple[0]
        gene_name = gene_tuple[6]
        gene_list.append((gene_ID, gene_name))
    return render_template("./view.html", gene_list = gene_list)

@app.route("/Genes/view/<id>")
def gene_by_ID(id):
    data = get_gene_by_ID(id)
    gene = build_gene_dict(data[0])
    transcripts = get_transcript_list(id)
    return render_template("./gene_by_ID.html", gene = gene, transcripts = transcripts, id=id )

@app.route("/Genes/del/<id>", methods=['POST'])
def del_gene(id):
    delete_gene(id)
    return redirect(url_for("/Genes"))

@app.route("/Genes/new", methods=['GET','POST'])
def add_gene():
    if request.method == 'GET': # if GET print the form
        return render_template("./new.html")
    else: # if POST return the answers
        return render_template("./new.html")

if __name__ == "__main__":
    db_file = "static/ensembl_hs63_simple.sqlite"
    app.run(debug=True)
else:
    db_file = '/home/amren/tp_prog_web/static/ensembl_hs63_simple.sqlite'
