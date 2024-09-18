## My Personal/Blog Website 

#### **You can see it *[here](https://pouriamoradpour.pythonanywhere.com/)***

## A Brief Story/Documentation

I do a lot of writing—about my _many_ thoughts on _many_ things! Recently, I was suggested a few times to publish my work. I also build a lot of projects—which I would love others to see. So, I took the next step like a developer(!): create a solution for it!
## _As Simple As It Gets_: What It Is
 It's simple: a homepage with what I felt was the right combination of flair and simplicity, pretty user authentication pages (login/sign-up), and the page you're currently viewing: an article page that is easy on eyes and doesn't prioritize form over function. It also supports text formatting, image embedding, etc., in the articles.
## _My Site, My Choice!_: Design, Technical Choices, and Overview
Since it was a Django application from the start, creating a static website wasn’t an option—especially with the roadmap I had in mind that required backend functionality. At the same time, the project didn’t demand a heavy JavaScript framework, so I opted for Materialize CSS, a responsive front-end framework inspired by Google’s Material Design principles (with a fork still maintained by the community).

[![website-as-a-whole.png](https://i.postimg.cc/nVGpX7v1/website-as-a-whole.png)](https://postimg.cc/s1xt8MHB)
#### "_Looks Good to Me_": Visual Design
I've always loved dark themes and have questioned the existence of light ones! I’m also especially fond of teal and orange-like colors. That essentially led me to this design: a dark theme with different tones of teal and amber as accent colors. Except, when it comes to the article page. I prioritized readability and used the good old white text over dark grey, spacing the lines a little more and slightly enlarging the text compared to a regular paragraph tag.
#### _Not Over-Engineered, Just Future-Proof_: Back-End
I kept the future roadmap in mind when designing the database, so I wouldn’t have to make major changes as I add new features that require access to or collection of more data. That’s why some features might seem over-engineered or unnecessary for the website at its current state.

For all my fellow database nerds out there, my schema for this website _does_ comply with 4NF & BCNF. Although, admittedly, this is not a complex design, and Django's ORM handles a lot of the heavy lifting. So normalizing such a database wasn’t a difficult task.
[![db-drawing.png](https://i.postimg.cc/fy2PxwWM/db-drawing.png)](https://postimg.cc/N2Xbtvrn)
I am currently using the SQLite database that Django itself provides, but I will soon switch to a proper MySQL or PostgreSQL database. Most of my views are Django's Generic Views, with a few methods overridden—mainly to track and save data, and protect it at the DB level. The Sign-Up view is still quite trivial and uses Django's `UserCreationForm` to add users to the `User` model (handled by signals to create a corresponding record in the `UserProfileModel`).
##### "_Fine, I'll Do It Myself_": Automating Deployment
Due to some limitations that I’ll get to later, I was forced to host my website on PythonAnywhere (although I plan to change that soon), which doesn’t provide an automated deployment feature like Railway or Render.

[![pipeline-drawing.png](https://i.postimg.cc/GhtVbszt/pipeline-drawing.png)](https://postimg.cc/KRXJNj6h)
So, I created a simple _what you could call a CI/CD pipeline_ (without tests, for now): a webhook on GitHub that sends a POST request to a view on my website whenever a commit is pushed. This triggers a Bash script that pulls the changes, migrates the database, and collects the static files. In non-technical terms, the website automatically updates itself whenever a change is made to its code.
##### "_Markdown In - HTML Out_": Text Formatting Within the Article
I tend to do my writing in Obsidian, which uses Markdown syntax—and I’m very comfortable with it. That’s why I added functionality to submit my posts in Markdown syntax and see them rendered in the article page. I achieved this using Markdownx, which handles everything: from the editing space to live preview (though I use Obsidian instead anyway), to a DB field and the conversion of Markdown to HTML for rendering on the browser.

[![website-as-a-whole.png](https://i.postimg.cc/nVGpX7v1/website-as-a-whole.png)](https://postimg.cc/s1xt8MHB)

Read The Full Documentation here *[here](https://pouriamoradpour.pythonanywhere.com/article/4/)*
