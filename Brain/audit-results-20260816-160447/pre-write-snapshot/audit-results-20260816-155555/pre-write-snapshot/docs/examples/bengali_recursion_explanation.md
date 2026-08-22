# Bengali Technical Learning: Recursion

This document shows a bilingual Bengali-English explanation of recursion.

---

## Explanation

**Recursion (রিকার্সন)** হলো এমন একটি প্রোগ্রামিং পদ্ধতি যেখানে একটি ফাংশন নিজেকে নিজেই কল (call) করে।

সহজ কথায় বোঝানোর জন্য একটি বাস্তব উদাহরণ দেওয়া যাক:
ধরুন আপনি একটি লাইনে দাঁড়িয়ে আছেন এবং জানতে চান আপনার সামনে কতজন মানুষ দাঁড়িয়ে আছে। আপনি আপনার সামনের জনকে জিজ্ঞেস করলেন, "আপনার সামনে কয়জন আছে?" সেও তার সামনের জনকে একই প্রশ্ন করলো। এভাবে প্রশ্নটি লাইনের একেবারে সামনে থাকা প্রথম মানুষের কাছে পৌঁছাবে। প্রথম মানুষটি যখন উত্তর দেবে "আমার সামনে কেউ নেই (০ জন)", তখন তার পেছনের জন তার সাথে ১ যোগ করে তার পেছনের জনকে উত্তর দেবে। এভাবে উত্তরটি আপনার কাছে এসে পৌঁছাবে।

এই উদাহরণে:
- **Base Case**: যখন লাইনের প্রথম মানুষের সামনে কেউ থাকে না (০ জন)। অর্থাৎ, যেখানে লুপ বা কল শেষ হবে।
- **Recursive Case**: যখন একজন মানুষ তার সামনের জনের উত্তর পাওয়ার পর তার সাথে ১ যোগ করে পেছনে পাঠায়।

---

## Python Implementation

```python
def count_people_ahead(position):
    # Base Case: If you are at the front of the line
    if position == 0:
        return 0
    # Recursive Case: 1 + count of people ahead of the person in front of you
    else:
        return 1 + count_people_ahead(position - 1)
```

এখানে `count_people_ahead` ফাংশনটি নিজেকেই আবার প্যারামিটার `position - 1` দিয়ে কল করছে, যতক্ষণ না এটি `position == 0` (Base Case) স্পর্শ করে।
