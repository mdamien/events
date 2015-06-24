#!/usr/bin/ruby

require 'json'
require 'nokogiri'

URL = "https://www.couchsurfing.com/events/search/PAGE?utf8=%E2%9C%93" +
      "&search_type=event&search_query=Paris%2C+France&latitude=48.856614" +
      "&longitude=2.3522219&country=&region="

events = []

def curl(url)
  `#{File.read('curl').gsub('URL_PLACEHOLDER', url)}`
end

def cached_curl(url)
  file = "tmp/url-#{url.gsub(/[^a-z0-9]+/i, '-')}"
  if File.exists?(file)
    File.read(file)
  else
    return ""
    sleep 2
    content = curl(url)
    File.write(file, content)
    content
  end
rescue
  ""
end

30.times do |page|
  res = cached_curl(URL.gsub('PAGE', page.to_s))
  doc = Nokogiri::HTML(res)

  selector = '.search-results-list .card.event-item .card__title a'
  events += doc.css(selector).map do |el|
    cached_curl("https://www.couchsurfing.com/#{el['href'].to_s}")
  end
end

events.map! { |event| Nokogiri::HTML(event) }

events.map! do |e|
  image = e.at_css(".cs-image-with-text img")
  image = image ? image["src"] : ""
  times = e.at_css(".cs-event-time")
  next unless times
  times = times.text.strip.split('—').map(&:strip)

  {
    title: e.at_css(".cs-image-with-text figcaption h1").text,
    start_at: times.first,
    end_at: times.last,
    location: e.at_css(".cs-event-details li a:first").text,
    description: e.at_css("meta[name=description]")['content'],
    url: e.at_css("link[rel=canonical]")['href'],
    image: image
  }
end

File.write('cs.json', JSON.pretty_generate(events.compact))
