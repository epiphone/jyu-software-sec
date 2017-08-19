import lxml.html
import lxml.html.clean
import slimit.ast
import slimit.parser
import lab6visitor

from debug import *

libcode = '''
<script>
    var sandbox_document = {
        getElementById: function(id) {
            var e = document.getElementById('sandbox-' + id);
            return {
                get onclick() { return e.onclick; },
                set onclick(h) {
                  e.onclick = function(evt) {
                    if (evt) {
                      // evt.target is read-only so using Object.create instead:
                      evt = Object.create(evt, {
                        target: {
                          value: {
                            ownerDocument: {
                              defaultView: sandbox_window
                            }
                          }
                        }
                      })
                    }
                    return h(evt)
                  }
                },
                get textContent() { return e.textContent; },
                set textContent(h) { e.textContent = h; },
            }
        }
    };

    var sandbox_eval = function(str) {
        return undefined
    }

    var sandbox_setTimeout = function(fn, ms) {
        var isString = typeof fn === 'string' || fn instanceof String
        fn.toString = fn.__proto__.toString
        return isString ? Object.__invalid__ : setTimeout(fn, ms)
    }

    var sandbox_window = {
      eval: sandbox_eval
    }

    var sandbox_Function = function() {
      return Function.__invalid__
    }

    function this_check(that) {
        return that == window ? Object.__invalid__ : that
    }

    function bracket_check(id) {
        var dangerous = ['__proto__', 'constructor', '__defineGetter__', '__defineSetter__']
        id.toString = id.__proto__.toString
        id.valueOf = id.__proto__.valueOf
        return dangerous.indexOf(id) >= 0 ? '__invalid__' : id
    }

    Object.__proto__.__invalid__ = function() { return this.__invalid__ }
    Object.__proto__.__invalid__.eval = Object.__invalid__
    String.prototype.__invalid__ = Object.__invalid__

    // Do not change these functions.
    function sandbox_grader(url) {
        window.location = url;
    }
    function sandbox_grader2() {
        eval("1 + 1".toString());  // What could possibly go wrong...
    }
    function sandbox_grader3() {
        try {
            eval(its_okay_no_one_will_ever_define_this_variable);
        } catch (e) {
        }
    }
</script>
'''

def filter_html_cb(s, jsrewrite):
    cleaner = lxml.html.clean.Cleaner()
    cleaner.scripts = False
    cleaner.style = True
    doc = lxml.html.fromstring(s)
    clean = cleaner.clean_html(doc)
    for el in clean.iter():
        if el.tag == 'script':
            el.text = jsrewrite(el.text)
            for a in el.attrib:
                del el.attrib[a]
        if 'id' in el.attrib:
            el.attrib['id'] = 'sandbox-' + el.attrib['id']
    return lxml.html.tostring(clean)

@catch_err
def filter_js(s):
    parser = slimit.parser.Parser()
    tree = parser.parse(s)
    visitor = lab6visitor.LabVisitor()
    return visitor.visit(tree)

@catch_err
def filter_html(s):
    return libcode + filter_html_cb(s, filter_js)

