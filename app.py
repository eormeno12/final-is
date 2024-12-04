from flask import Flask, jsonify, request, Response
import datetime

app = Flask(__name__)


data = {
  "users": [
    {
      "alias": "user1",
      "name": "User 1",
      "contacts": [],
      "sentMessages": [],
      "receivedMessages": []
    },
    {
      "alias": "user2",
      "name": "User 2",
      "contacts": [],
      "sentMessages": [],
      "receivedMessages": []
    },
    {
      "alias": "user3",
      "name": "User 3",
      "contacts": [],
      "sentMessages": [],
      "receivedMessages": []
    }
  ]
}


users = data["users"]


def get_user(alias):
  for user in users:
    if user["alias"] == alias:
      return user
  return None


def create_user(alias, name):
  user = get_user(alias)
  
  if user:
    return None
    
  new_user = {
    "alias": alias,
    "name": name,
    "contacts": [],
    "sentMessages": [],
    "receivedMessages": []
  }
  
  users.append(new_user)
  
  return new_user


def get_contacts(alias):
  user = get_user(alias)
  if user:
    return jsonify(user["contacts"])
  return None


def add_contact(alias, name, contact_alias):
  user = get_user(alias)
  
  if not user:
    return Response("The user does not exist.", status=404)
  
  contacts_aliases = [contact["alias"] for contact in user["contacts"]]
  if contact_alias in contacts_aliases:
    return Response("The contact is already in the contacts list.", status=400)

  contact = get_user(contact_alias)
  
  if not contact:
    if name:
      contact = create_user(contact_alias, name)
    else:
      return Response("The contact does not exist.", status=404)
  
  
  user["contacts"].append({
    "alias": contact["alias"],
    "registeredAt": datetime.datetime.now().isoformat()
  })
  
  return jsonify(user["contacts"])


def send_message(sender_alias, receiver_alias, content):
  sender = get_user(sender_alias)
  receiver = get_user(receiver_alias)
  
  if not sender:
    return Response("The sender does not exist.", status=404)
  
  if not receiver:
    return Response("The receiver does not exist.", status=404)
  
  contacts_aliases = [contact["alias"] for contact in sender["contacts"]]
  if receiver_alias not in contacts_aliases:
    return Response("The receiver is not in the contacts list.", status=400)
  
  message_body = {
    "content": content,
    "sentAt": datetime.datetime.now().isoformat()
  }
  
  sender["sentMessages"].append({
    "receiver": receiver_alias,
    **message_body
  })
  
  receiver["receivedMessages"].append({
    "sender": sender_alias,
    **message_body
  })
  
  return jsonify(message_body)


def message_history(alias):
  user = get_user(alias)
  if user:
    return jsonify(user["receivedMessages"])

  return None


@app.route("/mensajeria/contactos", methods=["GET"])
def get_contacts_route():
  alias = request.args.get("mialias")
  return get_contacts(alias)


@app.route("/mensajeria/contactos/<alias>", methods=["POST"])
def add_contact_route(alias):
  data = request.json
  name = data.get("nombre", None)
  contact_alias = data["contacto"]
  return add_contact(alias, name, contact_alias)


@app.route("/mensajeria/enviar", methods=["POST"])
def send_message_route():
  data = request.json
  sender_alias = data["usuario"]
  receiver_alias = data["contacto"]
  content = data["mensaje"]
  return send_message(sender_alias, receiver_alias, content)


@app.route("/mensajeria/recibidos", methods=["GET"])
def message_history_route():
  alias = request.args.get("mialias")
  return message_history(alias)


if __name__ == "__main__":
    app.run(debug=True)

