from giftpal import create_app
from giftpal import run_scheduler

if __name__ == '__main__':
    app = create_app()
    run_scheduler()
    app.run(debug=True)