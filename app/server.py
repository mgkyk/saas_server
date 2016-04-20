##
# this file is used to operate some command in server
#
# __author__: chuxiaokai
# data: 2016/3/28
import os
from app.models import *

"""
some operation on server
"""
class Server(object):
    ip = "127.0.0.1"  # default ip

    # hash_id = 0

    def __init__(self):
        """
        get server ip, initial the server
        :return:
        """
        # get the server ip
        return_info = (os.popen('ifconfig|(grep "net addr" & grep "255.255.255.0")')).readlines()
        if len(return_info) == 1:
            self.ip = (return_info[0].split('net addr:')[1]).split(' ')[0]
        else:
            print('Failed find the server ip')

    def init_machine(self, image_id):
        """
		init a docker container
		:return: container_id, passwd='123456'
		"""
        os.system("docker run -it -d=true '%s' /bin/bash" % image_id)  # create a machine
        container_id = (os.popen('docker ps -l -q')).readlines()[0].split('\n')[0]  # get the container's id
        container_ip = (os.popen('docker inspect --format="{{.NetworkSettings.IPAddress}}" %s' % container_id)).readlines()[0]
        os.system('docker exec %s service sshd start' % container_id)  # start the ssh service
        return container_id, "123456", container_ip

    def kill_machine(self, container_id):
        """
        stop a docker container and delete it
        """
        os.system("docker kill %s" % container_id)
        os.system("docker rm %s" % container_id)
        return True

    def exec_shell(self, shell_path, param, state):
        """
        :param shell_path: the path of the shell
        :param param: param: a list or a single string
        :return:
        """
        if state == 'cluster':
            shell = "bash "+shell_path
            for i in range(len(param)):
                shell = shell + ' ' + param[i]
            print(shell)

            if os.system(shell) == 0:
                return True
            else:
                return False
        else:
            shell = "bash "+shell_path+' '+param
            if os.system(shell) == 0:
                return True
            else:
                return False

    def get_machine_state(self, container_id):
        """
        :param container_id:
        :return: the load of a mc
        """
        if os.path.exists('shell/report.sh)'):
            print("shell/report.sh is not found")
            return False
        else:
            get_ret = (os.popen('bash shell/report.sh "%s"' % container_id)).readlines()
            ret_info = {'cpu info': get_ret[0], 'disk info': get_ret[1], 'memory info': get_ret[2], 'IDLE info': get_ret[3]}
            print(ret_info)
            return ret_info

    def install_software(self, user_name, shell_path, src_name, map, num_node):
        """
        install a software named src_name
        :param user_name:
        :param shell_path:
        :param src_name:
        :param map:
        :param num_node:
        :return:
        """
        if map == 'cluster':
            containers = []
            container_ips = []
            for i in range(num_node):
                container_id, passwd, container_ip = self.init_machine('666cb2f7a158')
                containers.append(container_id)
                container_ips.append(container_ip)
            print(containers)
            # self.exec_shell(shell_path, containers, state='cluster')
            # write in the db
            # write table vm_machine
            for i in range(num_node):
                new_mc = VM_machine(mc_id=containers[i], user=user_name, apply_info=str(user_name)+'_'+str(src_name), state='ON')
                db.session.add(new_mc)
            # write table user
            user = db.session.query(User).filter(User.user==user_name).first()
            source_info = user.source_info
            source_info = source_info + str(src_name) + ': ' + str(num_node) + 'nodes-> '+container_ips[0]+'(mgmd), ' + ', '.join(container_ips[1:]) + ';'
            db.session.query(User).filter(User.user==user_name).update({User.source_info: source_info})
            db.session.commit()
        else:
            container_id, passwd, container_ip = self.init_machine('ff416b30c157')
            # self.exec_shell(shell_path, container_id, state='single')
            string = user_name + '_' + src_name
            print(string)
            new_mc = VM_machine(mc_id=container_id, user=user_name, apply_info=string, state='ON')
            db.session.add(new_mc)
            user = db.session.query(User).filter(User.user==user_name).first()
            source_info = user.source_info
            source_info = source_info + str(src_name) + '-> ' + container_ip + ';'
            db.session.query(User).filter(User.user==user_name).update({User.source_info:source_info})
            db.session.commit()

