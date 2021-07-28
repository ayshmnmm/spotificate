# Spotificate

A python web app deployed on heroku that shows your spotify stats. Uses flask and spotipy. Check it out [here](https://spotificate.herokuapp.com/)


## Running locally

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

* Git clone into your local repository.
* Flask and spotify packages are used, use pip or something similar to install them.
* Get your client id and secret from the spotify developer dashboard page. Create an app if you don't have one already.
* Add http://127.0.0.1:5000/callback to the redirect uris in your app settings.

### Set up and run

Change the value of localrun variable in main.py to True and use your spotify client id and secret.

```python
localrun = True
cid = os.environ.get('CLID', 'insert client id') # spotify client id
secret = os.environ.get('SECR', 'insert client secret') # spotify client secret
```

Now run wsgi.py and visit http://127.0.0.1:5000 in your browser.

## Built Using

* [Mobirise](https://mobirise.com/) - Frontend 
* [Flask](https://flask.palletsprojects.com/) - Web framework 
* [Spotipy](https://spotipy.readthedocs.io/) - Python library for the spotify web api

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE) file for details

## Acknowledgments

* Hat tip to anyone whose code was used

## To dos

Only displays top tracks of user as of now
* Display more data such as average danceability of songs, valence(mood) of recent songs and more..
* Use matplotlib or any other library to display visualizations of the data.
* Stop using mobirise and make frontend lighter






