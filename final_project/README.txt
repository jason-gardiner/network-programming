Ports Used

HOST = "localhost"
PORT = 10000


Running The Chatroom

1) Run the server.py file

2) Make sure you can have multiple instances of the client.py file running

3) Open any number of the client.py file


Using The Chatroom

1) Do no put spaces in your screen name

2) End any message with EXIT to disconnect

3) To private message someone, use @their_screen_name at the start of your message

4) A message that is not determined to be private will be broadcast to all connected users


Example Inputs/Outputs

1) Input: Hello there
   Output: ['BROADCAST', 'Screen_Name', 'Hello there']

2) Input: @User1 My social security number is **** *** ****
   Output: ['PRIVATE', 'User1', '@User1 My social security number is **** *** ****']

3) Input: I'm logging off EXIT
   Output: ['BROADCAST', 'Screen_Name', "I'm logging off "]
           Successfully disconnected from server.

4) Input: EXIT
   Output: Successfully disconnected from server.