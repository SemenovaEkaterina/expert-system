'use strict';

/*

Main javascript functions to init most of the elements

#1. MENU RELATED STUFF
#2. CONTENT SIDE PANEL TOGGLER
#3. OUR OWN CUSTOM DROPDOWNS 
#4. BOOTSTRAP RELATED JS ACTIVATIONS
#5. TODO Application

*/

// ------------------------------------
// HELPER FUNCTIONS TO TEST FOR SPECIFIC DISPLAY SIZE (RESPONSIVE HELPERS)
// ------------------------------------

function is_display_type(display_type) {
    return $('.display-type').css('content') == display_type || $('.display-type').css('content') == '"' + display_type + '"';
}

function not_display_type(display_type) {
    return $('.display-type').css('content') != display_type && $('.display-type').css('content') != '"' + display_type + '"';
}

var drake;
$(function () {
    if (typeof dragula !== 'undefined') {
        drake = dragula({
            moves: function (el, container, handle) {
                return handle.classList.contains('drag-handle');
            }
        }).on('drag', function () {
        }).on('drop', function (el) {
        }).on('over', function (el, container) {
            $(container).closest('.tasks-list').addClass('over');
        }).on('out', function (el, container, source) {
            var new_pipeline_body = $(container).closest('.tasks-list');
            new_pipeline_body.removeClass('over');
            var old_pipeline_body = $(source).closest('.tasks-list');
        });
    }
});

var addToDragula = function ($container) {
    if (typeof drake !== 'undefined') {
        $container.each(function (i, el) {
            drake.containers.push(el);
        });
    }
};

$(function () {
    // #1. MENU RELATED STUFF

    // INIT MOBILE MENU TRIGGER BUTTON
    $('.mobile-menu-trigger').on('click', function () {
        $('.menu-mobile .menu-and-user').slideToggle(200, 'swing');
        return false;
    });

    // INIT MENU TO ACTIVATE ON HOVER
    var menu_timer;
    $('.menu-activated-on-hover ul.main-menu > li.has-sub-menu').mouseenter(function () {
        var $elem = $(this);
        clearTimeout(menu_timer);
        $elem.closest('ul').addClass('has-active').find('> li').removeClass('active');
        $elem.addClass('active');
    });
    $('.menu-activated-on-hover ul.main-menu > li.has-sub-menu').mouseleave(function () {
        var $elem = $(this);
        menu_timer = setTimeout(function () {
            $elem.removeClass('active').closest('ul').removeClass('has-active');
        }, 200);
    });

    // INIT MENU TO ACTIVATE ON CLICK
    $('.menu-activated-on-click li.has-sub-menu > a').on('click', function (event) {
        var $elem = $(this).closest('li');
        if ($elem.hasClass('active')) {
            $elem.removeClass('active');
        } else {
            $elem.closest('ul').find('li.active').removeClass('active');
            $elem.addClass('active');
        }
        return false;
    });

    // #2. CONTENT SIDE PANEL TOGGLER

    $('.content-panel-toggler, .content-panel-close, .content-panel-open').on('click', function () {
        $('.all-wrapper').toggleClass('content-panel-active');
    });

    // #3. OUR OWN CUSTOM DROPDOWNS
    $('.os-dropdown-trigger').on('mouseenter', function () {
        $(this).addClass('over');
    }).on('mouseleave', function () {
        $(this).removeClass('over');
    });

    // #5. TODO Application

    // Tasks foldable trigger
    $('.tasks-header-toggler').on('click', function () {
        $(this).closest('.tasks-section').find('.tasks-list-w').slideToggle(100);
        return false;
    });

    // Sidebar Sections foldable trigger
    $('.todo-sidebar-section-toggle').on('click', function () {
        $(this).closest('.todo-sidebar-section').find('.todo-sidebar-section-contents').slideToggle(100);
        return false;
    });

    // Sidebar Sub Sections foldable trigger
    $('.todo-sidebar-section-sub-section-toggler').on('click', function () {
        $(this).closest('.todo-sidebar-section-sub-section').find('.todo-sidebar-section-sub-section-content').slideToggle(100);
        return false;
    });

    // Drag init
    if ($('.tasks-list').length && typeof dragula !== 'undefined') {
        // INIT DRAG AND DROP FOR Todo Tasks
        addToDragula($('.tasks-list'));
    }

    $('.tasks-list').on('click', '.task-btn-undelete', function () {
        $(this).closest('.draggable-task').removeClass('pre-removed');
        $(this).remove();
        if (typeof timeoutDeleteTask !== 'undefined') {
            clearTimeout(timeoutDeleteTask);
        }
        return false;
    });

    // ajax csrf
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    var csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        }
    });
});
