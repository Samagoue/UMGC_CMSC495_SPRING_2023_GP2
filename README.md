<h1 align="center">GiftPal</h1>
<h3 align="center">The Ultimate Gift Exchange and Reminder App</h3>

<p align="center">
<img alt="GiftPal" src="https://raw.githubusercontent.com/Samagoue/UMGC_CMSC495_SPRING_2023_GP2/master/giftpal/static/GiftPalLogo.png" width="220"/>
</br>
<a href="https://github.com/Samagoue/UMGC_CMSC495_SPRING_2023_GP2">
<img alt="MIT License" src="https://img.shields.io/github/license/Samagoue/UMGC_CMSC495_SPRING_2023_GP2.svg"/>
</a>
<a href="https://github.com/Samagoue/UMGC_CMSC495_SPRING_2023_GP2">
<img alt="Release" src="https://img.shields.io/github/release/Samagoue/UMGC_CMSC495_SPRING_2023_GP2.svg"/>
</a>
</p>

## Purpose

The topic of our project is an application that tracks your loved one's special dates and their wish lists. We have also added gift exchange functionality to our application. Our application will send emails reminding the user of their loved one's special dates and send emails informing users who they are paired with for the gift exchange and some suggestions of what to get them as a gift. 

## Building

Clone the repository:

    git clone https://github.com/Samagoue/UMGC_CMSC495_SPRING_2023_GP2.git

Access the cloned folder and run:

    docker build -t giftpal .

## Using

    docker run -p 5000:5000 giftpal

Access the application at http://localhost:5000

## License

This project is licensed under the MIT License.