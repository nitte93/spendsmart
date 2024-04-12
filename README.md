# spendsmart

# ssh
ssh -i ~/Downloads/LightsailDefaultKey-us-east-1.pem bitnami@67.202.58.96

# v env
python3 -m venv env 
source env/bin/activate

# postgres
Installation Directory: /Library/PostgreSQL/16
Server Installation Directory: /Library/PostgreSQL/16
Data Directory: /Library/PostgreSQL/16/data
Database Port: 5432
Database Superuser: postgres
Operating System Account: postgres
Database Service: postgresql-16
Command Line Tools Installation Directory: /Library/PostgreSQL/16
pgAdmin4 Installation Directory: /Library/PostgreSQL/16/pgAdmin 4
Stack Builder Installation Directory: /Library/PostgreSQL/16
Installation Log: /tmp/install-postgresql.log

# pip freeze
asgiref==3.8.1
Django==4.2.11
django-environ==0.11.2
psycopg==3.1.18
psycopg2-binary==2.9.9
sqlparse==0.4.4
typing_extensions==4.11.0

# run commands

// restart apache
sudo /opt/bitnami/ctlscript.sh restart apache

// apache server error log
tail -f /opt/bitnami/apache2/logs/error_log 

// apache server access log
tail -f /opt/bitnami/apache2/logs/access_log 

// apache running modules
sudo /opt/bitnami/apache/bin/apachectl -M

// to install to bitnami site-packages
sudo python3 -m pip install django-environ 
sudo python3 -m pip install djangorestframework django-cors-headers Markdown
https://docs.djangoproject.com/en/5.0/intro/tutorial02/



sudo /opt/bitnami/ctlscript.sh status

python3 manage.py runserver

sudo /opt/bitnami/ctlscript.sh restart postgresql

python3 -m django --version                                  

sudo /opt/bitnami/ctlscript.sh restart apache

// users running apache servr
ps aux | grep apache

// give write access
sudo chown -R daemon:root /opt/bitnami/projects/mysite/media/
sudo chmod -R 755 /opt/bitnami/projects/mysite/media/

python manage.py makemigrations

python manage.py migrate

python3 manage.py makemigrations polls

python3 manage.py shell


^Cbitnami@ip-172-26-10-146:/opt/bitnami/projects/mysite$ history
    1  ls
    2  cd stack
    3  ls
    4  cd ..
    5  cd /opt/bitnami/
    6  ls
    7  python -m django --version
    8  pyton -v
    9  python -v
   10  python -m pip install -U Django
   11  python -m django --version
   12  sudo mkdir -p /opt/bitnami/projects/mysite
   13  sudo chown -R $USER /opt/bitnami/projects
   14  sudo chown -R $USER /opt/bitnami/mysite
   15  cd /opt/bitnami/
   16  ls
   17  cd projects/
   18  ls
   19  django-admin startproject mysite
   20  django-admin startproject mysite /opt/bitnami/projects/mysite
   21  ls
   22  cd mysite
   23  ls
   24  cd mysite
   25  ls
   26  cd .
   27  cd
   28  ls
   29  cd ~
   30  ls
   31  cd /opt/
   32  ls
   33  cd bitnami/
   34  ls
   35  cd projects/
   36  ls
   37  django-admin version
   38  ls
   39  cd mysite/
   40  ls
   41  python manage.py startapp polls
   42  ls
   43  cd mysite
   44  ls
   45  cd ../polls/
   46  ls
   47  vi views.py
   48  ls
   49  cd..
   50  ls
   51  cd ..
   52  ls
   53  cd polls
   54  ls
   55  vi urls.py
   56  cd ..
   57  ls
   58  cd mysite/
   59  ls
   60  vi urls.py 
   61  cd ..
   62  ls
   63  cd mysite/
   64  ls
   65  python manage.py runserver
   66  cd mysite/
   67  vi urls.py 
   68  cd ..
   69  python manage.py runserver
   70  ls
   71  cd ..
   72  ls
   73  cd ..
   74  ls
   75  cd mysi
   76  ls
   77  cd projects/mysite/
   78  ls
   79  cd mysite/
   80  ls
   81  cat wsgi.py
   82  ls
   83  sudo cp /opt/bitnami/apache/conf/vhosts/sample-vhost.conf.disabled /opt/bitnami/apache/conf/vhosts/mysite-vhost.conf
   84  sudo cp /opt/bitnami/apache/conf/vhosts/sample-https-vhost.conf.disabled /opt/bitnami/apache/conf/vhosts/mysite-https-vhost.conf
   85  cd /opt/bitnami/apache/conf/
   86  ls
   87  cd vhosts/
   88  ls
   89  cat mysite-vhost.conf 
   90  cat mysite-https-vhost.conf 
   91  vi mysite-https-vhost.conf 
   92  vi mysite-vhost.conf 
   93  cat mysite-vhost.conf 
   94  vi mysite-vhost.conf 
   95  cat mysite-https-vhost.conf 
   96  vi mysite-https-vhost.conf 
   97  sudo /opt/bitnami/ctlscript.sh restart apache
   98  cd /opt/bitnami/projects/mysite/
   99  ls
  100  cd mysite/
  101  ls
  102  vi settings.py 
  103  cd ..
  104  ls
  105  python manage.py collectstatic --noinput
  106  cd mysite/
  107  vi settings.py 
  108  ls
  109  cd ..
  110  ls
  111  cd mysite/
  112  ls
  113  python manage.py collectstatic --noinput
  114  cd mysite/
  115  vi settings.py 
  116  cd ../
  117  python manage.py collectstatic --noinput
  118  ls
  119  cd static/
  120  ls
  121  cd admin/
  122  ls
  123  cd /opt/bitnami/apache/conf/
  124  ls
  125  vd vhosts/
  126  cd vhosts/
  127  ls
  128  cat mysite-vhost.conf 
  129  vi mysite-vhost.conf 
  130  ls
  131  vi mysite-https-vhost.conf 
  132  cat mysite-https-vhost.conf 
  133  sudo /opt/bitnami/ctlscript.sh restart apache
  134  cd /opt/bitnami/projects/mysite/
  135  ls
  136  python3 manage.py runserver 
  137  python3 manage.py runserver 67.202.58.96:80
  138  python3 manage.py migrate
  139  python3 manage.py runserver 67.202.58.96:80
  140  python3 manage.py runserver 0.0.0.0:80
  141  python3 manage.py runserver 
  142  vi mysite-https-vhost.conf 
  143  vi /opt/bitnami/apache
  144  clear
  145  cd /opt/bitnami/apache/conf/
  146  ls
  147  xs vhosts/
  148  cd vhosts/
  149  ls
  150  cat mysite-vhost.conf 
  151  vi  mysite-vhost.conf
  152  vi  mysite-https-vhost.conf 
  153  sudo /opt/bitnami/ctlscript.sh restart apache
  154  cd /opt/bitnami/projects/mysite/
  155  ls
  156  cd mysite/
  157  ls
  158  cat settings.py 
  159  python3 manage.py createsuperuser
  160  cd ..
  161  ls
  162  python3 manage.py createsuperuser
  163  sudo /opt/bitnami/ctlscript.sh restart apache
  164  vi  mysite-vhost.conf
  165  ls
  166  cd mysite/
  167  ls
  168  vi settings.py 
  169  sudo /opt/bitnami/ctlscript.sh restart apache
  170  python3 manage.py runserver 0.0.0.0:8000
  171  cd ..
  172  python3 manage.py runserver 0.0.0.0:8000
  173  sudo /opt/bitnami/ctlscript.sh restart apache
  174  python3 manage.py runserver 0.0.0.0:8000
  175  clear
  176  cd /opt/
  177  ls
  178  cd bitnami/
  179  ls
  180  sudo /opt/bitnami/ctlscript.sh -M
  181  dpkg -s libapache2-mod-wsgi
  182  cd ../../
  183  ls
  184  cd home/
  185  ls
  186  cd bitnami/
  187  l
  188  ls
  189  cd /opt/bitnami/projects/mysite/
  190  ls
  191  python3 manage.py runserver 0.0.0.0:8000
  192  ls
  193  cd mysite/
  194  ls
  195  cat urls.py 
  196  ls
  197  cd ..
  198  ls
  199  cd polls/
  200  l
  201  ls
  202  cat views.py 
  203  cd ,,
  204  cd ..
  205  ls
  206  cd ..
  207  ls
  208  cd mysite/
  209  ls
  210  python3 manage.py runserver 0.0.0.0:8000
  211  cd /opt/bitnami/apache/conf/
  212  ls
  213  cat httpd.conf 
  214  vi httpd.conf 
  215  ls
  216  vd vhosts/
  217  ls
  218  cd vhosts/
  219  ;s
  220  ls
  221  cat mysite-vhost.conf 
  222  sudo /opt/bitnami/ctlscript.sh restart apache
  223  clear
  224  cd /opt/bitnami/projects/
  225  ls
  226  cd mysite/
  227  ls
  228  ssh-keygen -t ed25519 -C "nitte.tiwari1993@gmail.com"
  229  cd /home/bitnami/.ssh
  230  ls
  231  eval "$(ssh-agent -s)"
  232  pbcopy < ~/.ssh/id_ed25519.pub
  233  cat  ~/.ssh/id_ed25519.pub
  234  cd /opt/bitnami/
  235  ls
  236  cd /home/bitnami/
  237  ls
  238  cd /opt/bitnami/projects/
  239  ls
  240  cd mysite/
  241  clear
  242  ls
  243  echo "# spendsmart" >> README.md
  244  ls
  245  git init
  246  ls
  247  git add -A
  248  git commit -m "first commit"
  249  clear
  250  git branch -M main
  251  git remote add origin git@github.com:nitte93/spendsmart.git
  252  git push -u origin main
  253  Niharikaa@0823jnp[]]\[
  254  ls
  255  exit
  256  clear
  257  PostgreSQL
  258  createuser -U postgres USER_NAME -S -D -R -P
  259  sudo /opt/bitnami/ctlscript.sh restart postgresql
  260  cd /opt/bitnami/
  261  ls
  262  cd postgresql/
  263  clear
  264  ls
  265  ifconfig -a
  266  exit
  267  cd /opt/bitnami/
  268  cd postgresql/
  269  ls
  270  clear
  271  ls
  272  cd conf/
  273  ls
  274  vi pg_hba.conf 
  275  ls
  276  sudo vi pg_hba.conf 
  277  sudo vi postgresql.conf 
  278  sudo /opt/bitnami/ctlscript.sh restart postgresql
  279  psql -U postgres
  280  cd .
  281  ls
  282  cd .
  283  cd 
  284  ls
  285  cat bitnami_credentials 
  286  cat bitnami_application_password 
  287  postgres --version
  288  exit
  289  sudo /opt/bitnami/ctlscript.sh status
  290  cat bitnami_credentials 
  291  cat /opt/bitnami/postgresql/conf/postgresql.conf
  292  cat /opt/bitnami/postgresql/conf/pg_hba.conf
  293  sudo /opt/bitnami/ctlscript.sh restart postgresql
  294  postgres --version
  295  cat bitnami_credentials 
  296  python -v
  297  clear
  298  cat bitnami_credentials 
  299  clear
  300  cd /opt/bitnami/projects/
  301  cd mysite/
  302  ls
  303  git pull
  304  ls
  305  cd mysite/
  306  ls
  307  touch .env
  308  vi .env
  309  python3 manage.py migrate
  310  cd ..
  311  python3 manage.py migrate
  312  pip3 install django-environ
  313  python3 manage.py migrate
  314  python3 manage.py runserver