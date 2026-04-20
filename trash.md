what is the diffence between them?:-

app.config['SECRET_KEY']='your_secret_key'
app.secret_key = "super_secret_key_here"
which one is correct?


what does this means:-
app.config["SECRET_KEY"] = "IF I WROTE THIS THEN WHAT IS THE MEANING OF THIS ?"

how flash works

To actually see the flash message, you need to use a template (.html file) and a special Flask function called get_flashed_messages().