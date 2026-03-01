module Jekyll

# concept_gen.rb
# Jason A. Heppler
# jasonheppler.org
# last modified: Thu Sep 27 16:34:12 2012
# 
# The concept_gen is for creating concept highlighting
# such as can be found on mountainmeadows.unl.edu. The 
# tagging system will work by wrapping the text you wish to
# highlight in the concept highlighting tags, for example:
#
# {% c %}this text will be highlighted{% ec %}
#
# Everything between the start of the concept (c) and the 
# end of the concept (ec) will be highlighted. 
#
# The concept_list will generate a list of concepts for the 
# given document and should be placed in the single.html _layout 
# file.

  # Create the starting tag
  class ConceptInlineTag < Liquid::Tag
    def initialize(tag_name, concepts, tokens)
      super 
      @concepts = concepts
    end

    def render(context)
      <<-HTML
<span title="#{@concepts}" style="background-color:transparent">
      HTML
    end
  end

  # Create the ending tag
  class ConceptEndTag < Liquid::Tag
    def render(context)
      <<-HTML
</span>
      HTML
    end
  end

  class ConceptList < Liquid::Tag
    def render(context)
      <<-HTML
        <span title="#{@concepts}" style="background-color:transparent; ">
          <a title="#{@concepts}" onmouseover="highlightSpan(this.getAttribute('title'))">
            Native Americans <br/>
            Members
          </a>
        </span>
      HTML
    end
  end

end

Liquid::Template.register_tag('c', Jekyll::ConceptInlineTag)
Liquid::Template.register_tag('ec', Jekyll::ConceptEndTag)
Liquid::Template.register_tag('concept_list', Jekyll::ConceptList)