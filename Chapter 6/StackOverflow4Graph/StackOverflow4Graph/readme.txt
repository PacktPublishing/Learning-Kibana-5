This CSV is a dump of StackOverflow posts downloaded on June 10th 2016 from
https://ia800500.us.archive.org/22/items/stackexchange/stackoverflow.com-Posts.7z

The questions and answers have been assembled into a single row with two fields:

* tag - a comma delimited list of tags used in a post 
* user - a comma delimited list of usernames/IDs who were involved in the post.

The IndexPosts Python script deletes then creates a “stackoverflow” index with
the data from the CSV file.

This makes a good demo of the Graph API, showing related tags and users 
(see https://twitter.com/elasticmark/status/742282644948430848 )