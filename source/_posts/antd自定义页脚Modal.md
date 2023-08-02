---
title: antd自定义页脚Modal
date: 2023-08-02 18:35:50
tags: [antd, Modal]
categories: 工作
---

需求：
{%asset_img  need.jpg 需求%}

## 前置背景：

用户登录成功后，如果当前状态为初始密码状态，则跳转到目标页面且展示弹窗提示用户修改密码。由于之前产品希望 modal 可以跨页面展示，所以没有使用 Modal 组件，而是使用了 Modal.confirm:

```javascript
Modal.confirm({
  content:
    res.is_user_password_expired === IsUserPasswordExpiredEnum.EXPIRE_SOON
      ? i18n.t('Login.Login.index.LOCALE_DEFAULT_SUFFIX3836')
      : i18n.t('Login.Login.index.firstLoginModifyPwd'),
  okText: i18n.t('commonGenerator.confirm_3'),
  cancelText: i18n.t('commonGenerator.cancel'),
  onOk: () => {
    // 防止用户在修改密码界面点击浏览器返回键或者取消，程序卡死
    dispatch(setIsLogin({ isLogin: true, token: res.token ?? '' }));
    history.push('/password_modify');
  },
  onCancel: () => {
    dispatch(setIsLogin({ isLogin: true, token: res.token ?? '' }));
    if (target) {
      window.location.href = target;
    }
  },
});
```

## 本次需求

产品希望在底部增加一个取消和确认之外的忽略按钮，点击忽略按钮时，调用新增的忽略密码提示接口，然后自动关闭弹窗。

### 首选方案：使用自定义页脚 footer 属性

```javascript
Modal.confirm({
  // ...
  footer:[{
    <Button key='1'>忽略</Button>,
    <Button key='2'>取消</Button>,
    <Button key='3'>确认</Button>
  }]
})
```

问题：目前项目使用的 antd 版本为 4.x,而 antd5.x 才支持 footer 属性，所以有两个选择：

1. 升级项目依赖库版本【暂时没有升级计划，直接忽略】
2. 通过非正常方式实现支持自定义页脚的 Modal

### 实现思路

#### 使用 Modal 组件封装一个支持自定义页脚的弹窗

```javascript
const [visible, setVisible] = useState(false);

const showModal = () => {
  setVisible(true);
};

const handleOk = () => {
  // ...handling
};

const handleCancel = () => {
  // ...handling
};

const handleIgnore = () => {
  // ...handling
};

return (
  <>
    <Button onClick={showModal}>Open Modal</Button>

    <Modal
      visible={visible}
      onOk={handleOk}
      onCancel={handleCancel}
      footer={[
        <Button key="cancel" onClick={handleCancel}>
          取消
        </Button>,

        <Button key="ignore" onClick={handleIgnore}>
          忽略
        </Button>,

        <Button key="submit" type="primary" onClick={handleOk}>
          确认
        </Button>,
      ]}
    >
      <p>Modal Content</p>
    </Modal>
  </>
);
```

由于 antd4.x 的 Modal 组件支持 footer 属性，所以可以通过该组件封装。但是问题是我们需要弹窗能跨页面展示。需要做到这一点，可以采用方案：使用 redux 将 modal 的显示状态提升到全局

```jsx
// store.js
export const store = createStore( reducer: (state, action) => {
  // ... handles modal visibility state
})

// App.js
<Provider store={store}>
  <Router>
    {/* 根据 redux state 来渲染 Modal */}
    <Modal />

    <Route path="/a" component={PageA} />
    <Route path="/b" component={PageB} />
  </Router>
</Provider>

// PageA.js
import { showModal } from './actions'

const openModal = () => {
  dispatch(showModal()) // 开启 modal
}

// PageB.js
// 这里不需要做任何处理,modal 会继续显示
```

但是这个弹窗并不是全局的功能，所以并不希望将其放置在全局的路由中，且这样做的话修改成本较高，所以放弃此方案。

### 最终方案

思路：cancelText 属性类型支持 ReactNode，所以可以考虑将忽略按钮和取消按钮同一看做是 cancelText,通过 CSS 和点击事件设置达到相同效果

```javascript
const handleIgnore = async (modal: any) => {
  const token = localStorage.getItem('token');
  dispatch(setIsLogin({ isLogin: true, token: token ?? '' }));
  const ignore = UserService.ignorePasswdChangeAlarm();
  modal.destroy();
  ignore.catch((err) => message.error(getErrorMessage(err)));
  if (target) {
    window.location.href = target;
  }
};
const handleCancel = (modal?: any) => {
  const token = localStorage.getItem('token');
  dispatch(setIsLogin({ isLogin: true, token: token ?? '' }));
  if (target) {
    window.location.href = target;
  }
  if (!!modal) {
    modal.destroy();
  }
};
const modal = Modal.confirm({
  // ....
  className: 'need-modify-modal',
  cancelText: (
    <>
      <Button onClick={() => handleIgnore(modal)}>忽略</Button>
      <Button onClick={() => handleCancel(modal)}>取消</Button>
    </>
  ),
  cancelButtonProps: {
    className: 'cancel-ignore-btns',
    onClick: () => {},
    type: 'text',
  },
});
```

此时再设置样式即可

```less
.need-modify-modal {
  .ant-modal-confirm-btns {
    display: flex;
    justify-content: end;
    align-items: center;
    border: none;
    .cancel-ignore-btns {
      border: none;
      display: flex;
      align-items: end;
      padding: 0;
      justify-content: end;
      width: 80%;
      cursor: default;
      > span {
        width: 100%;
        display: flex;
        justify-content: space-between;
        background-color: #fff;
      }
    }
  }
}
```
