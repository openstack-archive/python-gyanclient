2. Edit the ``/etc/gyanclient/gyanclient.conf`` file and complete the following
   actions:

   * In the ``[database]`` section, configure database access:

     .. code-block:: ini

        [database]
        ...
        connection = mysql+pymysql://gyanclient:GYANCLIENT_DBPASS@controller/gyanclient
