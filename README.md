# Distributed Timeline

In this project we built a distributed timeline service using kademilia as the core of our implementation. The system allows users to subscrive to other users in order to get their content, allows to publish content, and allows user to see their timeline, which consists in their own messages, and the ones published by users that are subscribed.

## 🔧 Installing Dependencies

Before running this project, you need to have `python3` and install the following dependencies using the following command:

```
pip3 install -r requirements.txt
```

## 🧰 Running Nodes

Our system has 2 kinds of nodes: `bootsrap` nodes and `normal` nodes. This is due to the usage of the kademlia algorithm. In order to run a `bootsrap` node run the following:

```
python3 peer.py
```

To run a `normal` node you need to specify an ip address, and 2 ports: one to be used by kademlia and another for tcp communication.

```
python3 peer.py -i 0.0.0.0 -p PORT -tcp PORT
```

## 🧪 Tests

This repository also contains a small test script create with the intent of understanding our application's limits. To do so you need to run:

```
./run-tests.sh
```

## 💪 Team

This project was built as part of **Distributed System in Large Scale @ University of Minho**:

* A34900 - [Cecília Soares](https://github.com/soaresCecilia)
* A84442 - [Diogo Ribeiro](https://github.com/ribeiropdiogo)
* A89982 - [Joel Ferreira](https://github.com/joel98ferreira)
* A84244 - [Luís Cunha](https://github.com/luiscvnha)
* A83712 - [Rui Mendes](https://github.com/ruimendes29)




