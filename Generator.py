import random
import collections

class vertex:
  word = ""
  total_range = -1
  def __init__(self, w):
    self.word = w

class edge:
  v = None
  count = -1
  min_range = -1
  max_range = -1
  def __init__(self, vert):
    self.v = vert
    self.count = 1


class Generator:
  vertices = dict()

  edges = collections.defaultdict(list)
  
  START_WORD = "@@@@@"

  END_WORD = "###"

  def __init__(self):
    self.add_vertex(self.START_WORD)
    self.add_vertex(self.END_WORD)
  
  def add_edge(self, w1, w2):
    if(not self.is_edge(w1, w2)):
      if(not self.is_vertex(w1)):
        self.add_vertex(w1)
      if(not self.is_vertex(w2)):
        self.add_vertex(w2)
      e = edge(self.vertices[w2])
      self.edges[w1].append(e)
      # print("Edge - {0} --> {1} - created.".format(w1, w2))
    else:
      for e in self.edges[w1]:
        if(e.v.word == w2):
          e.count += 1
          # print("Edge - {0} --> {1} - incremented.".format(w1, w2))

  def add_vertex(self, w):
    if(not self.is_vertex(w)):
      v = vertex(w)
      self.vertices[w] = v
    

  def populate(self, file):
    try:
      with open(file) as fi:
        content = fi.readlines()
        content = [x.strip() for x in content]
        # print (content)
        for line in content:
          prev_word = self.START_WORD
          curr_word = ""
          # print(line)
          words = line.split()
          # print(words)
          for word in words:
            # print(word)
            curr_word = word
            # print("Prev: {} Curr: {}".format(prev_word, curr_word))
            self.add_edge(prev_word, curr_word)
            prev_word = curr_word
          self.add_edge(curr_word, self.END_WORD)
    except IOError:
      print("ERROR: File {} failed to open.".format(file))
    fi.close()


  def set_probability(self):
    for v in self.vertices.values():
      prev_max = 0
      for e in self.edges[v.word]:
        e.min_range = prev_max
        e.max_range = prev_max + e.count
        prev_max = e.max_range
      v.total_range = prev_max

  def generate_sentence(self):
    random.seed()
    temp = self.START_WORD
    r = random.randrange(self.vertices[temp].total_range)
    sentence = []
    for e in self.edges[temp]:
      # print(e.v.word)
      if (r >= e.min_range and r < e.max_range):
        temp = e.v.word
        break
    
    while (temp is not self.END_WORD):
      # print (temp.total_range)
      sentence.append(temp)
      r = random.randrange(self.vertices[temp].total_range)
      # print ("Random: {}".format(r))
      for e in self.edges[temp]:
        if (r >= e.min_range and r < e.max_range):
          temp = e.v.word
          break

    generated_sentence = ""
    for word in sentence:
      generated_sentence += word + " "

    return generated_sentence

  def is_vertex(self, w):
    for v in self.vertices.values():
      if(v.word == w):
        return True
    return False

  def is_edge(self, w1, w2):
    if(self.is_vertex(w1) and self.is_vertex(w2)):
      if w1 in self.edges.keys():
        for e in self.edges[w1]:
          if(e.v.word == w2):
            return True
    return False

