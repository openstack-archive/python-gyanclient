Prerequisites
-------------

Before you install and configure the gyan service,
you must create a database, service credentials, and API endpoints.

#. To create the database, complete these steps:

   * Use the database access client to connect to the database
     server as the ``root`` user:

     .. code-block:: console

        $ mysql -u root -p

   * Create the ``gyanclient`` database:

     .. code-block:: none

        CREATE DATABASE gyanclient;

   * Grant proper access to the ``gyanclient`` database:

     .. code-block:: none

        GRANT ALL PRIVILEGES ON gyanclient.* TO 'gyanclient'@'localhost' \
          IDENTIFIED BY 'GYANCLIENT_DBPASS';
        GRANT ALL PRIVILEGES ON gyanclient.* TO 'gyanclient'@'%' \
          IDENTIFIED BY 'GYANCLIENT_DBPASS';

     Replace ``GYANCLIENT_DBPASS`` with a suitable password.

   * Exit the database access client.

     .. code-block:: none

        exit;

#. Source the ``admin`` credentials to gain access to
   admin-only CLI commands:

   .. code-block:: console

      $ . admin-openrc

#. To create the service credentials, complete these steps:

   * Create the ``gyanclient`` user:

     .. code-block:: console

        $ openstack user create --domain default --password-prompt gyanclient

   * Add the ``admin`` role to the ``gyanclient`` user:

     .. code-block:: console

        $ openstack role add --project service --user gyanclient admin

   * Create the gyanclient service entities:

     .. code-block:: console

        $ openstack service create --name gyanclient --description "gyan" gyan

#. Create the gyan service API endpoints:

   .. code-block:: console

      $ openstack endpoint create --region RegionOne \
        gyan public http://controller:XXXX/vY/%\(tenant_id\)s
      $ openstack endpoint create --region RegionOne \
        gyan internal http://controller:XXXX/vY/%\(tenant_id\)s
      $ openstack endpoint create --region RegionOne \
        gyan admin http://controller:XXXX/vY/%\(tenant_id\)s
