// pages/ranks/ranks.js
const app = getApp()
Page({

  /**
   * 页面的初始数据
   */
  data: {
    userInfo: {},
    hasUserInfo: false,
    canIUse: wx.canIUse('button.open-type.getUserInfo'),
    ranklist: [],
    userrank: 0,
    userscore: 0,
    pagenum: 1,
    allpages: 0
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    if (app.globalData.userInfo) {
      this.setData({
        userInfo: app.globalData.userInfo,
        hasUserInfo: true
      })
    } else if (this.data.canIUse) {
      // 由于 getUserInfo 是网络请求，可能会在 Page.onLoad 之后才返回
      // 所以此处加入 callback 以防止这种情况
      app.userInfoReadyCallback = res => {
        this.setData({
          userInfo: res.userInfo,
          hasUserInfo: true
        })
      }
    } else {
      // 在没有 open-type=getUserInfo 版本的兼容处理
      wx.getUserInfo({
        success: res => {
          app.globalData.userInfo = res.userInfo
          this.setData({
            userInfo: res.userInfo,
            hasUserInfo: true
          })
        }
      })
    }
    var that = this
    wx.request({
      url: 'http://127.0.0.1:5000/login',
      method: 'GET',
      data: {
        pages: this.data.pagenum
      },
      success: function (res) {
        // success
        console.log('submit success');
        that.setData({
          ranklist: res.data.ranks,
          allpages: res.data.allpages
        })
      }
    })
    wx.request({
      url: 'http://127.0.0.1:5000/userRank',
      method: 'GET',
      data: {
        username: this.data.userInfo.nickName
      },
      success: function (res) {
        console.log('submit success');
        that.setData({
          userrank: res.data.rank,
          userscore: res.data.score,
        })
      }
    }) 
  },
  pre: function () {
    this.setData({
      pagenum: this.data.pagenum - 1
    })
    this.onLoad();
  },
  next: function () {
    this.setData({
      pagenum: this.data.pagenum + 1
    })
    this.onLoad();
  },
  getUserInfo: function (e) {
    console.log(e)
    app.globalData.userInfo = e.detail.userInfo
    this.setData({
      userInfo: e.detail.userInfo,
      hasUserInfo: true
    })
  }

})