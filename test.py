import matplotlib.pyplot as plt


x = list([1, 2, 3, 4, 5, 6])
# corresponding y axis values
y = list([2, 4, 1, 5, 2, 6])

x.append(7)
y.append(2)

# plotting the points
plt.plot(x, y, color='green', linestyle='solid', linewidth=3,
         marker='o', markerfacecolor='blue', markersize=10)

# setting x and y axis range
plt.ylim(1, 8)
plt.xlim(1, 8)

# naming the x axis
plt.xlabel('x - axis')
# naming the y axis
plt.ylabel('y - axis')

# giving a title to my graph
plt.title('Some cool customizations!')

# function to show the plot
plt.show()

# stream = wallStreetBets.stream.comments()
#
# t2 = time.time()
# print(t2)
# for comment in stream:
#
#     print(comment)
#     print(comment.created_utc)
#     # print(comment.submission.title)
#
#     if time.time() - t2 > 20:
#         break
#
# print("____________________________________________________")
#
# time.sleep(10)
#
# for comment in stream:
#     print(comment)
#     print(comment.created_utc)