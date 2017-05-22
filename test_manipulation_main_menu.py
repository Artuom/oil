import subscriber

sub = subscriber.Subscriber('375259092515')
sub.level_up(0)
print sub.answer_text()[0]
print '\n'

print sub.answer_text()
sub.level_up(1)
print "Vveli 1=> \n", sub.answer_text()[0]

print '\n'
sub = subscriber.Subscriber('375259092515')
sub.level_up(0)

print sub.answer_text()
sub.level_up(2)
print "Vveli 2=> \n", sub.answer_text()[0]

print '\n'
sub = subscriber.Subscriber('375259092515')
sub.level_up(0)

print sub.answer_text()
sub.level_up(3)
print "Vveli 3=> \n", sub.answer_text()[0]

print '\n'
sub = subscriber.Subscriber('375259092515')
sub.level_up(0)

print sub.answer_text()
sub.level_up(4)
print "Vveli 4(incorrect input)=> \n", sub.answer_text()[0]

print '\n'
sub = subscriber.Subscriber('375259092515')
sub.level_up(0)

print sub.answer_text()
sub.level_up('a')
print "Vveli a(incorrect input)=> \n", sub.answer_text()[0]

