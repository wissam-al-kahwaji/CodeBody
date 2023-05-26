# Code Body 

> You can see a simple demo of the site *[Video Demo](https://fb.watch/kGeZRzTJCO/)*


**About Code Body**

> This is a Beta version of Code Body, you can take advantage of this version, as stated in the license

- On this website, you will find many features that you can try out and explore, such as the Quick Search experience, which can be accessed by using the shortcut `Ctrl + F`.

- Discussion: You can access the discussion section using the shortcut `Ctrl + D`. Inside the discussion, you can write using markdown formatting. You can also send within any form using `Ctrl + S`.

- Profile: Inside the personal account, you can format it using markdown formatting as well.

- You will find a "rank" field, which is available for future versions.
     - Additionally, CodeCoin is intended for future versions as well.

- SSE (Server-Sent Events) is used to update discussions, comments, and notifications.

- The `function` is used to adjust the image size.

AJAX is used throughout the majority of the website. You can see this.



## How can you get started?

> It is better to use virtualenv.
>> I am using sqlite, it will be easy to get started.

**step 1**

```python
pip install -r requirements.txt 
```
**step 2**
```python 
python manage.py makemigrations
```
**step 3**

```python 
python manage.py migrate
```

#### By Wissam Al-Kahwaji
