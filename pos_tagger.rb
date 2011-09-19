  require 'rubygems'
  require 'engtagger'

  # Create a parser object
  tgr = EngTagger.new

  if( ARGV.size != 2) then
    puts "usage: ruby pos_tagger.rb <text-in-quotes> <outputfile>"
    exit 1
  end
      
  # reading from the command line.
  text = ARGV[0]

  # opening output file.
  f = File.open(ARGV[1],"w")
  
  # Add part-of-speech tags to text
  tagged = tgr.add_tags(text)

  f.puts tagged
  f.close()
