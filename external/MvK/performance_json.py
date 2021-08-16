from mvk.mvk import MvK
from mvk.impl.python.datavalue import LocationValue

from mvk.impl.python.util.jsonserializer import MvKEncoder
from mvk.impl.client.jsondeserializer import MvKDecoder

import time

encoder = MvKEncoder()
decoder = MvKDecoder()

mvk = MvK()

start = time.time()
a = mvk.read(LocationValue("protected.formalisms.ActionLanguage"))
print("READ: " + str(time.time() - start))

start = time.time()
a = encoder.encode(a)
print("SERIALIZE: " + str(time.time() - start))

start = time.time()
for i in range(100):
    decoder.decode(a)
print("DESERIALIZE: " + str(time.time() - start))
