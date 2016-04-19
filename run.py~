from app import app, db
from app.models import *

if __name__ == '__main__':
    db.create_all()
    # insert into new resource
    # mysql = Resource("MySQL", "single node", "../shell/mysql_singlenode/MySQL_setup.sh", "Installing MySQL in your computer")
    # mysql_cluster = Resource('MySQL-Cluster', 'cluster', '../shell/mysql_cluster/MySQL_Cluster_setup.sh', 'Installing MySQL Cluster in your cluster')
    # db.session.add(mysql)
    # db.session.add(mysql_cluster)
    # db.session.commit()
    app.run(debug=True, use_reloader=False)
