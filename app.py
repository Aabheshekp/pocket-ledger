import csv, sqlite3, tkinter as tk
from datetime import date
from pathlib import Path
from tkinter import ttk, messagebox, filedialog
DB=Path(__file__).with_name('pocket-ledger.sqlite3')
class Ledger(tk.Tk):
 def __init__(self):
  super().__init__();self.title('Pocket Ledger');self.geometry('840x560');self.minsize(720,460);self.configure(bg='#f4f6f2');self.db=sqlite3.connect(DB);self.db.row_factory=sqlite3.Row;self.db.execute('CREATE TABLE IF NOT EXISTS expenses(id INTEGER PRIMARY KEY,date TEXT NOT NULL,description TEXT NOT NULL,category TEXT NOT NULL,amount REAL NOT NULL CHECK(amount>0))');self.build();self.refresh()
 def build(self):
  style=ttk.Style(self);style.theme_use('clam');style.configure('Treeview',rowheight=30,font=('Segoe UI',10));style.configure('Treeview.Heading',font=('Segoe UI',10,'bold'))
  head=tk.Frame(self,bg='#f4f6f2');head.pack(fill='x',padx=24,pady=(20,10));tk.Label(head,text='Pocket Ledger',font=('Segoe UI',24,'bold'),bg='#f4f6f2',fg='#183a2d').pack(anchor='w');tk.Label(head,text='A private, local-first view of everyday spending.',font=('Segoe UI',11),bg='#f4f6f2',fg='#637268').pack(anchor='w')
  form=ttk.LabelFrame(self,text='Add an expense',padding=12);form.pack(fill='x',padx=24,pady=8);self.vars={k:tk.StringVar(value=v) for k,v in [('date',date.today().isoformat()),('description',''),('category','Other'),('amount','')]}
  for i,(label,key) in enumerate([('Date (YYYY-MM-DD)','date'),('Description','description'),('Category','category'),('Amount','amount')]): ttk.Label(form,text=label).grid(row=0,column=i,sticky='w',padx=5);ttk.Entry(form,textvariable=self.vars[key],width=22).grid(row=1,column=i,padx=5,pady=4,sticky='ew')
  ttk.Button(form,text='Add expense',command=self.add).grid(row=1,column=4,padx=8);[form.columnconfigure(i,weight=1) for i in range(4)]
  bar=ttk.Frame(self);bar.pack(fill='x',padx=24,pady=8);self.total=tk.StringVar();ttk.Label(bar,textvariable=self.total,font=('Segoe UI',12,'bold')).pack(side='left');ttk.Button(bar,text='Delete selected',command=self.delete).pack(side='right',padx=5);ttk.Button(bar,text='Export CSV',command=self.export).pack(side='right',padx=5)
  self.tree=ttk.Treeview(self,columns=('date','description','category','amount'),show='headings');self.tree.pack(fill='both',expand=True,padx=24,pady=(4,20));[(self.tree.heading(c,text=t),self.tree.column(c,width=w,anchor=a)) for c,t,w,a in [('date','Date',120,'w'),('description','Description',360,'w'),('category','Category',160,'w'),('amount','Amount',120,'e')]]
 def add(self):
  try:
   d=self.vars['date'].get().strip();date.fromisoformat(d);desc=self.vars['description'].get().strip();cat=self.vars['category'].get().strip() or 'Other';amount=float(self.vars['amount'].get())
   if not desc or amount<=0:raise ValueError()
   self.db.execute('INSERT INTO expenses(date,description,category,amount) VALUES(?,?,?,?)',(d,desc,cat,amount));self.db.commit();self.vars['description'].set('');self.vars['amount'].set('');self.refresh()
  except ValueError:messagebox.showerror('Check expense','Enter a valid date, description, and amount greater than zero.')
 def refresh(self):
  for i in self.tree.get_children():self.tree.delete(i)
  rows=self.db.execute('SELECT * FROM expenses ORDER BY date DESC,id DESC').fetchall()
  for r in rows:self.tree.insert('', 'end',iid=str(r['id']),values=(r['date'],r['description'],r['category'],f"{r['amount']:.2f}"))
  month=date.today().strftime('%Y-%m');total=self.db.execute('SELECT COALESCE(SUM(amount),0) FROM expenses WHERE date LIKE ?', (month+'%',)).fetchone()[0];self.total.set(f'This month: {total:,.2f}   ·   {len(rows)} total entries')
 def delete(self):
  sel=self.tree.selection()
  if sel and messagebox.askyesno('Delete expense','Delete the selected expense?'):self.db.execute('DELETE FROM expenses WHERE id=?',(int(sel[0]),));self.db.commit();self.refresh()
 def export(self):
  name=filedialog.asksaveasfilename(defaultextension='.csv',filetypes=[('CSV','*.csv')])
  if name:
   rows=self.db.execute('SELECT date,description,category,amount FROM expenses ORDER BY date DESC').fetchall()
   with open(name,'w',newline='',encoding='utf-8') as f:w=csv.writer(f);w.writerow(['date','description','category','amount']);w.writerows([tuple(r) for r in rows])
   messagebox.showinfo('Export complete','CSV saved successfully.')
if __name__=='__main__':Ledger().mainloop()
