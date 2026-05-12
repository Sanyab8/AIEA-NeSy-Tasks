Task 4: Build Your Own KB

For this task, I learned how to use a logical reasoning engine with SWI-Prolog and Python. I created a small knowledge base about students and sports. The KB contains facts about students, sports, which sports students play, indoor sports, and team sports. The knowledge base includes more than 10 facts and multiple rules.

I used SWI-Prolog locally to load and test the KB. I ran queries such as `busy_player(bob).`, `plays_indoor(sanya).`, and `busy_player(X).`. These queries tested both facts and rules. For example, Bob is considered a busy player because he plays more than one sport.

One issue I encountered was a syntax error caused by forgetting a period after a fact. I also had issues installing the Janus SWI-Prolog Python package because of Git safe directory errors on Windows. After fixing the Git configuration and reinstalling the package, I was able to connect Python with SWI-Prolog successfully.

I then created a Python script (`test.py`) using `janus_swi` to run the same Prolog queries from Python. The Python results matched the SWI-Prolog results, confirming that the logical reasoning engine worked correctly in both environments.

This project helped me better understand how Prolog rules work using logical conditions and variable matching. I also learned how Prolog can integrate with Python for larger AI and reasoning systems.

GitHub Repo:
https://github.com/Sanyab8/AIEA-task4--Build-Your-Own-KB?utm_source=chatgpt.com