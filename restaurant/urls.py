from django.urls import path
from . import views

urlpatterns = [
    # Customer
    path('', views.table_selection, name='table_selection'),
    path('takeaway/', views.takeaway_menu, name='takeaway'),
    path('table/<int:table_id>/menu/', views.menu_view, name='menu'),
    path('order/place/', views.place_order, name='place_order'),
    path('order/<int:order_id>/status/', views.order_status, name='order_status'),
    path('order/<int:order_id>/bill/', views.bill_view, name='bill'),
    path('order/<int:order_id>/bill/download/', views.download_bill, name='download_bill'),
    path('order/<int:order_id>/pay-online/', views.pay_online, name='pay_online'),
    path('order/<int:order_id>/confirm-payment/', views.confirm_payment, name='confirm_payment'),
    path('order/<int:order_id>/reorder/', views.reorder, name='reorder'),
    path('order/<int:order_id>/reorder-menu/', views.reorder_menu, name='reorder_menu'),
    path('order/<int:order_id>/add-items/', views.add_items_to_order, name='add_items_to_order'),
    path('order/<int:order_id>/print-bill/', views.print_bill, name='print_bill'),

    # Customer auth & history
    path('customer/login/', views.customer_login, name='customer_login'),
    path('customer/home/', views.customer_history, name='customer_home'),
    path('customer/logout/', views.customer_logout, name='customer_logout'),
    path('customer/history/', views.customer_history, name='customer_history'),

    # Live Order page
    path('live-order/', views.live_order, name='live_order'),
    path('live-order/data/', views.live_order_data, name='live_order_data'),
    path('combo/<int:combo_id>/detail/', views.combo_detail_api, name='combo_detail'),

    # POS Terminal
    path('pos/', views.pos_portal, name='pos_portal'),
    path('pos/terminal/', views.pos_terminal, name='pos_terminal'),
    path('pos/save-draft/', views.pos_save_draft, name='pos_save_draft'),
    path('pos/save-order/', views.pos_save_order, name='pos_save_order'),
    path('pos/save-draft-no-auth/', views.pos_save_draft_no_auth, name='pos_save_draft_no_auth'),
    path('pos/drafts/', views.pos_get_drafts, name='pos_get_drafts'),
    path('pos/draft/<int:draft_id>/delete/', views.pos_delete_draft, name='pos_delete_draft'),

    # Staff
    path('staff/', views.staff_portal, name='staff_portal'),
    path('staff/login/', views.staff_login, name='staff_login'),
    path('staff/logout/', views.staff_logout, name='staff_logout'),
    path('staff/order/<int:order_id>/update/', views.update_order_status, name='update_order_status'),
    path('staff/orders/pending/', views.pending_orders_api, name='pending_orders_api'),
    path('staff/orders/reorders/', views.reorder_notification_api, name='reorder_notification_api'),
    path('staff/export/excel/', views.export_excel, name='export_excel'),
    path('staff/export/daily/', views.export_daily_excel, name='export_daily_excel'),
    path('staff/export/weekly/', views.export_weekly_excel, name='export_weekly_excel'),
    path('staff/export/monthly/', views.export_monthly_excel, name='export_monthly_excel'),
    path('staff/export/range/', views.export_range_excel, name='export_range_excel'),
    path('staff/qr-codes/', views.download_qr_codes, name='download_qr_codes'),
]
