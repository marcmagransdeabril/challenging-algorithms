
import bisect
import unittest

class ServerPartioner:
    def __init__(self):
        self._servers = []
        self._server2blob = {}

    def addServer(self,hostname):
        server = (hash(hostname),hostname)
        pos = bisect.bisect_left(self._servers,server)
        
        # if the server already exist, ignore
        if pos < len(self._servers) and self._servers[pos] == server:
            return

        self._servers.insert(pos,server)

        # Once the server is inserted, we need to re-partition the blob's in pos+1

        pos = (pos + 1) % len(self._servers)
        repartition_host = self._servers[pos][0]
        if repartition_host in self._server2blob and self._server2blob[repartition_host]:
            repartion_blobs = self._server2blob[repartition_host]
            self._server2blob[repartition_host] = set()
            for blob in repartion_blobs:
                self.addBlob(blob)


    def removeServer(self,hostname):
        server = (hash(hostname),hostname)
        pos = bisect.bisect_left(self._servers,server)

        # if the server does not exist, do not raise
        if pos > len(self._servers)-1 or self._servers[pos] != server:
            return

        # If there are blobs in the server retrieve them

        repartion_blobs = set()
        if hostname in self._server2blob and self._server2blob[hostname]:
            repartion_blobs = self._server2blob[hostname]

        # Remove the server

        self._servers.pop(pos)
        if hostname in self._server2blob:
            self._server2blob.pop(hostname)

        # Repartition the blobs if there is a host, otherwise just remove them, too
        if self._servers:
            for blob in repartion_blobs:
                self.addBlob(blob)

    def getClosestServer(self,blob):
        if not self._servers:
            Exception("No servers present. Can not associate blob to server")

        blob = (hash(blob),"")
        pos = bisect.bisect_right(self._servers,blob)

        if pos > len(self._servers)-1:
            return self._servers[0][1]
        else:
            return self._servers[pos][1]

    def getServer(self,blob):
        if not self._servers:
            Exception("No servers present. Can not associate blob to server")

        hostname = self.getClosestServer(blob)

        if hostname in self._server2blob:
            return hostname
        else:
            raise "Blob is not present in ny of the servers"


    def addBlob(self,blob):
        hostname = self.getClosestServer(blob)

        if hostname in self._server2blob:
            self._server2blob[hostname].add(blob)
        else:
            self._server2blob[hostname] = set([blob])

    def removeBlob(self,blob):
        try:
            hostname = self.getClosestServer(blob)
        except:
            # removal of unexisting blobs does not throw
            return

        if hostname in self._server2blob:
            self._server2blob[hostname].remove(blob)

class TestServerPartioner(unittest.TestCase):

    def test_server_not_present(self):
        p = ServerPartioner()

        with self.assertRaises(Exception):
            p.addBlob("myblob")

        p.removeBlob("myblob")

        p.addServer("my.host")

        self.assertEqual(len(p._servers),1)

        p.addServer("my.host")

        self.assertEqual(len(p._servers),1)

        p.removeServer("my.host")

        self.assertEqual(len(p._servers),0)

    def test_blob_present(self):
        p = ServerPartioner()

        p.addServer("my.host")

        with self.assertRaises(Exception):
            p.getServer("myblob")

        self.assertEqual(p.getClosestServer("anyblob"),"my.host")

        p.addBlob("myblob")

        self.assertEqual(p.getClosestServer("myblob"),"my.host")
        self.assertEqual(p.getServer("myblob"),"my.host")
    
    def test_repartition(self):
        p = ServerPartioner()

        p.addServer("my.host1")

        p.addBlob("myblob")

        self.assertEqual(p.getServer("myblob"),"my.host1")

        p.addServer("my.host2")
        p.removeServer("my.host1")

        self.assertEqual(p.getServer("myblob"),"my.host2")

    def test_multiple(self):
        p = ServerPartioner()

        p.addServer("my.host1")
        p.addServer("my.host2")
        p.addServer("my.host3")
        p.addServer("my.host1")
        p.addServer("my.host2")
        p.addServer("my.host3")

        self.assertEqual(len(p._servers), 3)


        p.addBlob("myblob1")
        p.addBlob("myblob2")
        p.addBlob("myblob3")
        p.addBlob("myblob4")

        self.assertEqual( sum([len(blobs) for blobs in p._server2blob.values()]), 4)
        p.getServer("myblob1")
        p.getServer("myblob2")
        p.getServer("myblob3")
        p.getServer("myblob4")

        p.removeServer("my.host1")
        self.assertEqual(len(p._servers), 2)
        self.assertEqual( sum([len(blobs) for blobs in p._server2blob.values()]), 4)
       
        p.removeBlob("myblob1")
        self.assertEqual( sum([len(blobs) for blobs in p._server2blob.values()]), 3)

        p.removeServer("my.host2")
        self.assertEqual(len(p._servers), 1)
        self.assertEqual( sum([len(blobs) for blobs in p._server2blob.values()]), 3)

        p.removeServer("my.host3")
        self.assertEqual(len(p._servers), 0)
        self.assertEqual( sum([len(blobs) for blobs in p._server2blob.values()]), 0)
