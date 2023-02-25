from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import database

##
# @file server.py
# @brief This file allows the user to interact with the main file (database) throught a website
# @author THARAUD Valentin & SAUVAGE Eli
# @version 1.0
# @date 07/06/2021

##
# @brief This is the main Class using the http.server package
class Serv(BaseHTTPRequestHandler):
    ##
    # @brief GET requests function
    # every GET request that arrives to the server goes throught here, we then test for the right route(path) to know what to send back
    # @param self default param for a class method
    # @return None
    def do_GET(self):
        if self.path == '/':
            file_to_open = open("./views/index.html").read()
            self.send_response(200)
            self.end_headers()
            self.wfile.write(bytes(file_to_open, 'utf-8'))

        elif self.path == "/js/index.js":
            file_to_open = open("./views/js/index.js").read()
            self.send_response(200)
            self.end_headers()
            self.wfile.write(bytes(file_to_open, 'utf-8'))

        elif self.path == "/js/jquery.min.js":
            file_to_open = open("./views/js/jquery.min.js").read()
            self.send_response(200)
            self.end_headers()
            self.wfile.write(bytes(file_to_open, 'utf-8'))

        elif self.path == "/bootstrap.min.css": 
            file_to_open = open("./views/bootstrap.min.css").read()
            self.send_response(200)
            self.end_headers()
            self.wfile.write(bytes(file_to_open, 'utf-8'))
        
        elif self.path == "/js/bootstrap.min.js":
            file_to_open = open("./views/js/bootstrap.min.js").read()
            self.send_response(200)
            self.end_headers()
            self.wfile.write(bytes(file_to_open, 'utf-8'))

        elif self.path == "/js/poper.min.js":
            file_to_open = open("./views/js/poper.min.js").read()
            self.send_response(200)
            self.end_headers()
            self.wfile.write(bytes(file_to_open, 'utf-8'))
    ##
    # @brief POST requests function
    # every POST request that arrives to the server goes throught here, we then test for the right route(path) to know what to read, what to modify in the database and to know what to send back
    # @param self default param for a class method
    # @return None
    def do_POST(self):
        if(self.path == "/newMemb"):
            content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
            post_data = self.rfile.read(content_length) # <--- Gets the data itself
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            if newMemb(json.loads(post_data.decode('utf-8'))):
                self.wfile.write(bytes(json.dumps({"response":"ok", "code":0}), "utf-8"))
            else:
                self.wfile.write(bytes(json.dumps({"response":"alreadyTaken", "code":1}), "utf-8"))
        if(self.path == "/editUser"):
            content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
            post_data = self.rfile.read(content_length) # <--- Gets the data itself
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            editUser(json.loads(post_data.decode('utf-8')))
            self.wfile.write(bytes(json.dumps({"response":"ok", "code":0}), "utf-8"))
        elif(self.path == "/delUser"):
            content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
            post_data = self.rfile.read(content_length).decode("utf-8") # <--- Gets the data itself
            database.DeleteUser(json.loads(post_data)["username"])
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(bytes("ok", "utf-8"))

        elif self.path == "/getUsers":
            content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
            post_data = self.rfile.read(content_length).decode("utf-8") # <--- Gets the data itself
            # print(post_data)
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            users = [user.export() for user in database.SearchForUser(post_data)]
            # print(users)
            self.wfile.write(bytes(json.dumps(users), "utf-8"))
        elif(self.path == "/follow"):
            content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
            post_data = self.rfile.read(content_length).decode("utf-8") # <--- Gets the data itself
            data = json.loads(post_data)
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            # print(data)
            if database.FindUsername(data["userToFollow"]):
                if data["follow"]:
                    database.Follow(data["user"], data["userToFollow"])
                else:
                    database.UnFollow(data["user"], data["userToFollow"])
                self.wfile.write(bytes(json.dumps({"response":"ok", "code":0, "newList":database.FindUsername(data["user"]).export()["iFollow"]}), "utf-8"))
            else:
                self.wfile.write(bytes(json.dumps({"response":"notFound", "code":1, "newList":database.FindUsername(data["user"]).export()["iFollow"]}), "utf-8"))

##
# @brief adds a new member to the database
# 
# @param memb dictionnary with the names of the fields of the html form as keys
# @return True if user created, False is pseudo already taken
def newMemb(memb):
    return database.CreateUser(memb["pseudo"], memb["name"], memb['age'], memb['year'], memb['field'], memb["city"], memb["areas"])

##
# @brief edit a member to the database
# 
# @param memb dictionnary with the names of the fields of the html form as keys
# @return None
def editUser(user):
    # print(user)
    database.UppdateUser(user["oldPseudo"], user['name'], user["age"], user["year"], user["field"], NewCity=user["city"], NewAreas=user["areas"])

httpd = HTTPServer(('127.0.0.1',8080),Serv)
httpd.serve_forever()