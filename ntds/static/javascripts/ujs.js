(function($, undefined) {

    /**
     * Unobtrusive scripting adapter for jQuery
     * https://github.com/ujs/jquery-ujs
     *
     * Requires jQuery 1.8.0 or later.
     *
     * Released under the MIT license
     *
     */

    // Cut down on the number of issues from people inadvertently including jquery_ujs twice
    // by detecting and raising an error when it happens.
    if ( $.ujs !== undefined ) {
        $.error('jquery-ujs has already been loaded!');
    }

    // Shorthand to make it a little easier to call public ujs functions from within ujs.js
    var ujs;
    var $document = $(document);

    $.ujs = ujs = {
        // Link elements bound by jquery-ujs
        linkClickSelector: 'a[data-confirm], a[data-method], a[data-remote], a[data-disable-with], a[data-disable]',

        // Button elements bound by jquery-ujs
        buttonClickSelector: 'button[data-remote]:not(form button), button[data-confirm]:not(form button)',

        // Select elements bound by jquery-ujs
        inputChangeSelector: 'select[data-remote], input[data-remote], textarea[data-remote]',

        // Form elements bound by jquery-ujs
        formSubmitSelector: 'form',

        // Form input elements bound by jquery-ujs
        formInputClickSelector: 'form input[type=submit], form input[type=image], form button[type=submit], form button:not([type]), input[type=submit][form], input[type=image][form], button[type=submit][form], button[form]:not([type])',

        // Form input elements disabled during form submission
        disableSelector: 'input[data-disable-with]:enabled, button[data-disable-with]:enabled, textarea[data-disable-with]:enabled, input[data-disable]:enabled, button[data-disable]:enabled, textarea[data-disable]:enabled',

        // Form input elements re-enabled after form submission
        enableSelector: 'input[data-disable-with]:disabled, button[data-disable-with]:disabled, textarea[data-disable-with]:disabled, input[data-disable]:disabled, button[data-disable]:disabled, textarea[data-disable]:disabled',

        // Form required input elements
        requiredInputSelector: 'input[name][required]:not([disabled]),textarea[name][required]:not([disabled])',

        // Form file input elements
        fileInputSelector: 'input[type=file]',

        // Link onClick disable selector with possible reenable after remote submission
        linkDisableSelector: 'a[data-disable-with], a[data-disable]',

        // Button onClick disable selector with possible reenable after remote submission
        buttonDisableSelector: 'button[data-remote][data-disable-with], button[data-remote][data-disable]',

        // Make sure that every Ajax request sends the CSRF token
        CSRFProtection: function(xhr) {
            var token = $('meta[name="csrf-token"]').attr('content');
            if (token) xhr.setRequestHeader('X-CSRF-Token', token);
        },

        // making sure that all forms have actual up-to-date token(cached forms contain old one)
        refreshCSRFTokens: function(){
            var csrfToken = $('meta[name=csrf-token]').attr('content');
            var csrfParam = $('meta[name=csrf-param]').attr('content');
            $('form input[name="' + csrfParam + '"]').val(csrfToken);
        },

        // Triggers an event on an element and returns false if the event result is false
        fire: function(obj, name, data) {
            var event = $.Event(name);
            obj.trigger(event, data);
            return event.result !== false;
        },

        // Default confirm dialog, may be overridden with custom confirm dialog in $.ujs.confirm
        confirm: function(message) {
            return confirm(message);
        },

        // Default ajax function, may be overridden with custom function in $.ujs.ajax
        ajax: function(options) {
            return $.ajax(options);
        },

        // Default way to get an element's href. May be overridden at $.ujs.href.
        href: function(element) {
            return element.attr('href');
        },

        // Submits "remote" forms and links with ajax
        handleRemote: function(element) {
            var method, url, data, elCrossDomain, crossDomain, withCredentials, dataType, options;

            if (ujs.fire(element, 'ajax:before')) {
                elCrossDomain = element.data('cross-domain');
                crossDomain = elCrossDomain === undefined ? null : elCrossDomain;
                withCredentials = element.data('with-credentials') || null;
                dataType = element.data('type') || ($.ajaxSettings && $.ajaxSettings.dataType);

                if (element.is('form')) {
                    method = element.attr('method');
                    url = element.attr('action');
                    data = element.serializeArray();
                    // memoized value from clicked submit button
                    var button = element.data('ujs:submit-button');
                    if (button) {
                        data.push(button);
                        element.data('ujs:submit-button', null);
                    }
                } else if (element.is(ujs.inputChangeSelector)) {
                    method = element.data('method');
                    url = element.data('url');
                    data = element.serialize();
                    if (element.data('params')) data = data + "&" + element.data('params');
                } else if (element.is(ujs.buttonClickSelector)) {
                    method = element.data('method') || 'get';
                    url = element.data('url');
                    data = element.serialize();
                    if (element.data('params')) data = data + "&" + element.data('params');
                } else {
                    method = element.data('method');
                    url = ujs.href(element);
                    data = element.data('params') || null;
                }

                options = {
                    type: method || 'GET', data: data, dataType: dataType,
                    // stopping the "ajax:beforeSend" event will cancel the ajax request
                    beforeSend: function(xhr, settings) {
                        if (settings.dataType === undefined) {
                            xhr.setRequestHeader('accept', '*/*;q=0.5, ' + settings.accepts.script);
                        }
                        if (ujs.fire(element, 'ajax:beforeSend', [xhr, settings])) {
                            element.trigger('ajax:send', xhr);
                        } else {
                            return false;
                        }
                    },
                    success: function(data, status, xhr) {
                        element.trigger('ajax:success', [data, status, xhr]);
                    },
                    complete: function(xhr, status) {
                        element.trigger('ajax:complete', [xhr, status]);
                    },
                    error: function(xhr, status, error) {
                        element.trigger('ajax:error', [xhr, status, error]);
                    },
                    crossDomain: crossDomain
                };

                // There is no withCredentials for IE6-8 when
                // "Enable native XMLHTTP support" is disabled
                if (withCredentials) {
                    options.xhrFields = {
                        withCredentials: withCredentials
                    };
                }

                // Only pass url to `ajax` options if not blank
                if (url) { options.url = url; }

                return ujs.ajax(options);
            } else {
                return false;
            }
        },

        // Handles "data-method" on links such as:
        // <a href="/users/5" data-method="delete" rel="nofollow" data-confirm="Are you sure?">Delete</a>
        handleMethod: function(link) {
            var href = ujs.href(link),
                method = link.data('method'),
                target = link.attr('target'),
                csrfToken = $('meta[name=csrf-token]').attr('content'),
                csrfParam = $('meta[name=csrf-param]').attr('content'),
                form = $('<form method="post" action="' + href + '"></form>'),
                metadataInput = '<input name="_method" value="' + method + '" type="hidden" />';

            if (csrfParam !== undefined && csrfToken !== undefined) {
                metadataInput += '<input name="' + csrfParam + '" value="' + csrfToken + '" type="hidden" />';
            }

            if (target) { form.attr('target', target); }

            form.hide().append(metadataInput).appendTo('body');
            form.submit();
        },

        // Helper function that returns form elements that match the specified CSS selector
        // If form is actually a "form" element this will return associated elements outside the from that have
        // the html form attribute set
        formElements: function(form, selector) {
            return form.is('form') ? $(form[0].elements).filter(selector) : form.find(selector);
        },

        /* Disables form elements:
         - Caches element value in 'ujs:enable-with' data store
         - Replaces element text with value of 'data-disable-with' attribute
         - Sets disabled property to true
         */
        disableFormElements: function(form) {
            ujs.formElements(form, ujs.disableSelector).each(function() {
                ujs.disableFormElement($(this));
            });
        },

        disableFormElement: function(element) {
            var method, replacement;

            method = element.is('button') ? 'html' : 'val';
            replacement = element.data('disable-with');

            element.data('ujs:enable-with', element[method]());
            if (replacement !== undefined) {
                element[method](replacement);
            }

            element.prop('disabled', true);
        },

        /* Re-enables disabled form elements:
         - Replaces element text with cached value from 'ujs:enable-with' data store (created in `disableFormElements`)
         - Sets disabled property to false
         */
        enableFormElements: function(form) {
            ujs.formElements(form, ujs.enableSelector).each(function() {
                ujs.enableFormElement($(this));
            });
        },

        enableFormElement: function(element) {
            var method = element.is('button') ? 'html' : 'val';
            if (element.data('ujs:enable-with')) element[method](element.data('ujs:enable-with'));
            element.prop('disabled', false);
        },

        /* For 'data-confirm' attribute:
         - Fires `confirm` event
         - Shows the confirmation dialog
         - Fires the `confirm:complete` event

         Returns `true` if no function stops the chain and user chose yes; `false` otherwise.
         Attaching a handler to the element's `confirm` event that returns a `falsy` value cancels the confirmation dialog.
         Attaching a handler to the element's `confirm:complete` event that returns a `falsy` value makes this function
         return false. The `confirm:complete` event is fired whether or not the user answered true or false to the dialog.
         */
        allowAction: function(element) {
            var message = element.data('confirm'),
                answer = false, callback;
            if (!message) { return true; }

            if (ujs.fire(element, 'confirm')) {
                answer = ujs.confirm(message);
                callback = ujs.fire(element, 'confirm:complete', [answer]);
            }
            return answer && callback;
        },

        // Helper function which checks for blank inputs in a form that match the specified CSS selector
        blankInputs: function(form, specifiedSelector, nonBlank) {
            var inputs = $(), input, valueToCheck,
                selector = specifiedSelector || 'input,textarea',
                allInputs = form.find(selector);

            allInputs.each(function() {
                input = $(this);
                valueToCheck = input.is('input[type=checkbox],input[type=radio]') ? input.is(':checked') : input.val();
                // If nonBlank and valueToCheck are both truthy, or nonBlank and valueToCheck are both falsey
                if (!valueToCheck === !nonBlank) {

                    // Don't count unchecked required radio if other radio with same name is checked
                    if (input.is('input[type=radio]') && allInputs.filter('input[type=radio]:checked[name="' + input.attr('name') + '"]').length) {
                        return true; // Skip to next input
                    }

                    inputs = inputs.add(input);
                }
            });
            return inputs.length ? inputs : false;
        },

        // Helper function which checks for non-blank inputs in a form that match the specified CSS selector
        nonBlankInputs: function(form, specifiedSelector) {
            return ujs.blankInputs(form, specifiedSelector, true); // true specifies nonBlank
        },

        // Helper function, needed to provide consistent behavior in IE
        stopEverything: function(e) {
            $(e.target).trigger('ujs:everythingStopped');
            e.stopImmediatePropagation();
            return false;
        },

        //  replace element's html with the 'data-disable-with' after storing original html
        //  and prevent clicking on it
        disableElement: function(element) {
            var replacement = element.data('disable-with');

            element.data('ujs:enable-with', element.html()); // store enabled state
            if (replacement !== undefined) {
                element.html(replacement);
            }

            element.bind('click.ujsDisable', function(e) { // prevent further clicking
                return ujs.stopEverything(e);
            });
        },

        // restore element to its original state which was disabled by 'disableElement' above
        enableElement: function(element) {
            if (element.data('ujs:enable-with') !== undefined) {
                element.html(element.data('ujs:enable-with')); // set to old enabled state
                element.removeData('ujs:enable-with'); // clean up cache
            }
            element.unbind('click.ujsDisable'); // enable element
        }
    };

    if (ujs.fire($document, 'ujs:attachBindings')) {

        $.ajaxPrefilter(function(options, originalOptions, xhr){ if ( !options.crossDomain ) { ujs.CSRFProtection(xhr); }});

        // This event works the same as the load event, except that it fires every
        // time the page is loaded.
        //
        // See https://github.com/ujs/jquery-ujs/issues/357
        // See https://developer.mozilla.org/en-US/docs/Using_Firefox_1.5_caching
        $(window).on("pageshow.ujs", function () {
            $($.ujs.enableSelector).each(function () {
                var element = $(this);

                if (element.data("ujs:enable-with")) {
                    $.ujs.enableFormElement(element);
                }
            });

            $($.ujs.linkDisableSelector).each(function () {
                var element = $(this);

                if (element.data("ujs:enable-with")) {
                    $.ujs.enableElement(element);
                }
            });
        });

        $document.delegate(ujs.linkDisableSelector, 'ajax:complete', function() {
            ujs.enableElement($(this));
        });

        $document.delegate(ujs.buttonDisableSelector, 'ajax:complete', function() {
            ujs.enableFormElement($(this));
        });

        $document.delegate(ujs.linkClickSelector, 'click.ujs', function(e) {
            var link = $(this), method = link.data('method'), data = link.data('params'), metaClick = e.metaKey || e.ctrlKey;
            if (!ujs.allowAction(link)) return ujs.stopEverything(e);

            if (!metaClick && link.is(ujs.linkDisableSelector)) ujs.disableElement(link);

            if (link.data('remote') !== undefined) {
                if (metaClick && (!method || method === 'GET') && !data) { return true; }

                var handleRemote = ujs.handleRemote(link);
                // response from ujs.handleRemote() will either be false or a deferred object promise.
                if (handleRemote === false) {
                    ujs.enableElement(link);
                } else {
                    handleRemote.fail( function() { ujs.enableElement(link); } );
                }
                return false;

            } else if (method) {
                ujs.handleMethod(link);
                return false;
            }
        });

        $document.delegate(ujs.buttonClickSelector, 'click.ujs', function(e) {
            var button = $(this);

            if (!ujs.allowAction(button)) return ujs.stopEverything(e);

            if (button.is(ujs.buttonDisableSelector)) ujs.disableFormElement(button);

            var handleRemote = ujs.handleRemote(button);
            // response from ujs.handleRemote() will either be false or a deferred object promise.
            if (handleRemote === false) {
                ujs.enableFormElement(button);
            } else {
                handleRemote.fail( function() { ujs.enableFormElement(button); } );
            }
            return false;
        });

        $document.delegate(ujs.inputChangeSelector, 'change.ujs', function(e) {
            var link = $(this);
            if (!ujs.allowAction(link)) return ujs.stopEverything(e);

            ujs.handleRemote(link);
            return false;
        });

        $document.delegate(ujs.formSubmitSelector, 'submit.ujs', function(e) {
            var form = $(this),
                remote = form.data('remote') !== undefined,
                blankRequiredInputs,
                nonBlankFileInputs;

            if (!ujs.allowAction(form)) return ujs.stopEverything(e);

            // skip other logic when required values are missing or file upload is present
            if (form.attr('novalidate') == undefined) {
                blankRequiredInputs = ujs.blankInputs(form, ujs.requiredInputSelector);
                if (blankRequiredInputs && ujs.fire(form, 'ajax:aborted:required', [blankRequiredInputs])) {
                    return ujs.stopEverything(e);
                }
            }

            if (remote) {
                nonBlankFileInputs = ujs.nonBlankInputs(form, ujs.fileInputSelector);
                if (nonBlankFileInputs) {
                    // slight timeout so that the submit button gets properly serialized
                    // (make it easy for event handler to serialize form without disabled values)
                    setTimeout(function(){ ujs.disableFormElements(form); }, 13);
                    var aborted = ujs.fire(form, 'ajax:aborted:file', [nonBlankFileInputs]);

                    // re-enable form elements if event bindings return false (canceling normal form submission)
                    if (!aborted) { setTimeout(function(){ ujs.enableFormElements(form); }, 13); }

                    return aborted;
                }

                ujs.handleRemote(form);
                return false;

            } else {
                // slight timeout so that the submit button gets properly serialized
                setTimeout(function(){ ujs.disableFormElements(form); }, 13);
            }
        });

        $document.delegate(ujs.formInputClickSelector, 'click.ujs', function(event) {
            var button = $(this);

            if (!ujs.allowAction(button)) return ujs.stopEverything(event);

            // register the pressed submit button
            var name = button.attr('name'),
                data = name ? {name:name, value:button.val()} : null;

            button.closest('form').data('ujs:submit-button', data);
        });

        $document.delegate(ujs.formSubmitSelector, 'ajax:send.ujs', function(event) {
            if (this == event.target) ujs.disableFormElements($(this));
        });

        $document.delegate(ujs.formSubmitSelector, 'ajax:complete.ujs', function(event) {
            if (this == event.target) ujs.enableFormElements($(this));
        });

        $(function(){
            ujs.refreshCSRFTokens();
        });
    }

})( jQuery );