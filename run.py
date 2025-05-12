#Use this for development server. for production server use run.bat
print('Use this for development server. for production server use run.bat')

from source.app import app

if __name__=='__main__':
    app.run(host='0.0.0.0', port='2568', debug=True)