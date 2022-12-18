from django.urls import path
from . import views
from .bank_admin_views import bank_admin_views
from .customer_views import customer_views
from .teller_views import teller_views
from .front_desk_views import front_desk_views
from .admin_transfer_views import admin_transfer_views
from .teller_transfer_views import teller_transfer_views
from .customer_to_customer_transfer_views import customer_to_customer_transfer_views


app_name = 'bank_admin'
urlpatterns = [
    path('', views.index, name='index'),
    # =======================Bank-Admin=============================#
    path('bank-admin/<uuid:admin>/', bank_admin_views.bankAdmin, name='bank-admin'),
    path('admin-register/', bank_admin_views.bankAdminRegister,
         name='admin-register'),
    path('login-admin/', bank_admin_views.LoginAdmin, name='login-admin'),
    path('admin-logout/<uuid:token>/',
         bank_admin_views.AdminLogout, name='admin-logout'),

    path('bank-admin-account-detail/<uuid:token>/', bank_admin_views.BankAdminAccountDetail,
         name='bank-admin-account-detail'),
    path('bank-admin-account-update/', bank_admin_views.BankAdminUpdateAccount,
         name='bank-admin-account-update'),
    path('bank-admin-update-status/<uuid:token>/', bank_admin_views.BankAdminUpdateAccountStatus,
         name='bank-admin-update-status'),

    # ========================Bank-Admin Operations==========================#
    path('get-teller-account/<uuid:token>/', bank_admin_views.PageTellerAccount,
         name='get-teller-account'),

    path('teller-detail-page/', bank_admin_views.TellerDetailPage,
         name='teller-detail-page'),

    path('get-all-tellers/<uuid:token>/', bank_admin_views.AllTellerPage,
         name='get-all-tellers'),

    path('teller-action/<uuid:teller_adminid>/<uuid:token>/', bank_admin_views.TellerAction,
         name='teller-action'),

    path('block-teller/<uuid:tellerid>/<uuid:token>/', bank_admin_views.BlockTeller,
         name='block-teller'),


    path('get-teller-number/<uuid:token>/', bank_admin_views.TellerAccountHistoryForm,
         name='get-teller-number'),

    path('teller-transaction-history/', bank_admin_views.TellerAccountHistory,
         name='teller-transaction-history'),

    path('transaction-history/<uuid:token>', bank_admin_views.TransactionHistory,
         name='transaction-history'),

    path('admin-transaction-history/<uuid:token>/', bank_admin_views.AdminTransactionHistory,
         name='admin-transaction-history'),

    path('transaction-detail/<uuid:transaction_ref>/<uuid:token>/', bank_admin_views.SingleTransactionHistory,
         name='transaction-detail'),

    path('admin-transfer-detail/<uuid:transaction_ref>/<uuid:token>/', bank_admin_views.SingleAdminTransferHistory,
         name='admin-transfer-detail'),

    path('delete-transaction/<uuid:transaction_ref>/<uuid:token>/', bank_admin_views.DeleteTransaction,
         name='delete-transaction'),

    path('delete-transfer/<uuid:transaction_ref>/<uuid:token>/', bank_admin_views.DeleteTransfer,
         name='delete-transfer'),
    # ===========================================================#
    # ===============================================================#


    # ========================Front-Desk==========================#
    path('front-desk/<uuid:token>/', front_desk_views.Dashboard, name='front-desk'),
    path('front-desk-register/', front_desk_views.FrontDeskRegister,
         name='front-desk-register'),
    path('front-desk-login/', front_desk_views.FrontDeskLogin,
         name='front-desk-login'),
    path('front-desk-logout/<uuid:token>/', front_desk_views.FrontDeskLogout,
         name='front-desk-logout'),
    path('account-detail/<uuid:token>/', front_desk_views.FrontDeskAccountDetail,
         name='account-detail'),
    path('update-account/', front_desk_views.UpdateAccount,
         name='update-account'),
    path('update-status/<uuid:token>/', front_desk_views.UpdateAccountStatus,
         name='update-status'),
    # ========================Front-Desk Operations==========================#
    path('get-customer-account/<uuid:token>/', front_desk_views.PageCustomerAccount,
         name='get-customer-account'),

    path('customer-detail-page/', front_desk_views.CustomerDetailPage,
         name='customer-detail-page'),

    path('get-all-customers/<uuid:token>/', front_desk_views.AllCustomerPage,
         name='get-all-customers'),

    path('customer-action/<uuid:customer_accountid>/<uuid:token>/', front_desk_views.CustomerAction,
         name='customer-action'),

    path('block-customer/<uuid:customerid>/<uuid:token>/', front_desk_views.BlockCustomer,
         name='block-customer'),

    path('update-customer-account-form/<uuid:customerid>/<uuid:token>/', front_desk_views.CustomerUpdateForm,
         name='update-customer-account-form'),

    path('customer-update-account/', front_desk_views.UpdateCustomerAccount,
         name='customer-update-account'),

    path('get-customer-number/<uuid:token>/', front_desk_views.CustomerAccountHistoryForm,
         name='get-customer-number'),

    path('customer-transaction-history/', front_desk_views.CustomerAccountHistory,
         name='customer-transaction-history'),
    # ===========================================================#


    # =======================Bank Customer========================#
    path('dashboard/<uuid:customer>/',
         customer_views.Dashboard, name='dashboard'),
    path('customer-register/', customer_views.CustomerRegister,
         name='customer-register'),
    path('customer-login/', customer_views.CustomerLogin, name='customer-login'),
    path('customer-logout/<uuid:token>/',
         customer_views.CustomerLogout, name='customer-logout'),


    path('transaction-history/<uuid:customerid>/',
         customer_views.CustomerTransactionHistory, name='transaction-history'),

    path('transaction-history-detail/<uuid:transaction_ref>/<uuid:token>/',
         customer_views.CustomerTransactionHistoryDetail, name='transaction-history-detail'),
    # ===========================================================#


    # ======================Tellers===============================#
    path('teller-admin/<uuid:teller>/',
         teller_views.Dashboard, name='teller-admin'),
    path('teller-register/', teller_views.TellerRegister,
         name='teller-register'),
    path('teller-login/', teller_views.TellerLogin, name='teller-login'),
    path('teller-logout/<uuid:token>/',
         teller_views.TellerLogout, name='teller-logout'),

    path('teller-admin-account-detail/<uuid:token>/', teller_views.TellerAdminAccountDetail,
         name='teller-admin-account-detail'),
    path('teller-admin-account-update/', teller_views.TellerAdminUpdateAccount,
         name='teller-admin-account-update'),
    path('teller-admin-update-status/<uuid:token>/', teller_views.TellerAdminUpdateAccountStatus,
         name='teller-admin-update-status'),

    # ===========================================================#

    # ======================Admin Transfer===============================#
    path('teller-account/<uuid:token>/',
         admin_transfer_views.GetTeller, name='teller-account'),
    path('teller-number/',
         admin_transfer_views.GetTellerNumber, name='teller-number'),
    path('transfer-teller/', admin_transfer_views.TransferToTeller,
         name='transfer-teller'),


    path('add-fund/<uuid:token>/', admin_transfer_views.FundAdminAccount,
         name='add-fund'),
    path('add-fund-form/<uuid:token>/', admin_transfer_views.FundAdminAccountForm,
         name='add-fund-form'),

    # ===========================================================#

    # ======================Teller Transfer===============================#
    path('customer-account/<uuid:token>/',
         teller_transfer_views.GetCustomer, name='customer-account'),
    path('customer-detail/',
         teller_transfer_views.GetCustomerDetail, name='customer-detail'),
    path('transfer-customer/<uuid:token>/', teller_transfer_views.TransferToCustomer,
         name='transfer-customer'),

    # ===========================================================#

    # # ======================Customer To Customer Transfer===============================#
    path('receiver-account/<uuid:token>/',
         customer_to_customer_transfer_views.GetReceiver, name='receiver-account'),
    path('receiver-detail/',
         customer_to_customer_transfer_views.GetReceiversDetail, name='receiver-detail'),
    path('transfer-receiver/', customer_to_customer_transfer_views.TransferToReceiver,
         name='transfer-receiver'),

    # # ===========================================================#






]
