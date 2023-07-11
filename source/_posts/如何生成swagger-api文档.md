---
title: 如何生成swagger-api文档
date: 2023-02-02 00:37:39
tags: [GoLang]
categories: 后端
---
使用依赖库：https://github.com/swaggo/swag
### 在makefile中提供生成命令
```
##	genSwaggerDoc: generate swagger docs by swaggo/swag
.PHONY: genSwaggerDoc
genSwaggerDoc:
	swag init -g ./cmd/notepad-apiserver/apiserver.go
```
### apiserver.go
```go
package main

import (
	_ "github.com/earthaYan/notePad/docs"
	"github.com/gin-gonic/gin"
	swaggerFiles "github.com/swaggo/files"
	ginSwagger "github.com/swaggo/gin-swagger"
)

// @title	notepad api
// @version	1.0
// @description	This is a sample server celler server.
// @host	116.204.108.126:8080
// @BasePath	/v1
// @securityDefinitions.basic  BasicAuth
func main() {
	r := gin.Default()
	c := controller.NewController()
	v1 := r.Group("v1")
	{
		accounts := v1.Group("/accounts")
		{
			accounts.GET(":id", c.ShowAccount)
			accounts.GET("", c.ListAccounts)
			accounts.POST("", c.AddAccount)
			accounts.DELETE(":id", c.DeleteAccount)
			accounts.PATCH(":id", c.UpdateAccount)
			accounts.POST(":id/images", c.UploadAccountImage)
		}
		r.GET("/swagger/*any", ginSwagger.WrapHandler(swaggerFiles.Handler))
		r.Run(":8080")
	}
	log.Println("start http server")
	log.Fatal(http.ListenAndServe(":50052", nil))
}
```
### controller/accounts.go
```go
package controller

import (
	"fmt"
	"net/http"
	"strconv"

	"github.com/gin-gonic/gin"
	"github.com/swaggo/swag/example/celler/httputil"
	"github.com/swaggo/swag/example/celler/model"
)

// ShowAccount godoc
//
//	@Summary		Show an account
//	@Description	get string by ID
//	@Tags			accounts
//	@Accept			json
//	@Produce		json
//	@Param			id	path		int	true	"Account ID"
//	@Success		200	{object}	model.Account
//	@Failure		400	{object}	httputil.HTTPError
//	@Failure		404	{object}	httputil.HTTPError
//	@Failure		500	{object}	httputil.HTTPError
//	@Router			/accounts/{id} [get]
func (c *Controller) ShowAccount(ctx *gin.Context) {
	id := ctx.Param("id")
	aid, err := strconv.Atoi(id)
	if err != nil {
		httputil.NewError(ctx, http.StatusBadRequest, err)
		return
	}
	account, err := model.AccountOne(aid)
	if err != nil {
		httputil.NewError(ctx, http.StatusNotFound, err)
		return
	}
	ctx.JSON(http.StatusOK, account)
}

// ListAccounts godoc
//
//	@Summary		List accounts
//	@Description	get accounts
//	@Tags			accounts
//	@Accept			json
//	@Produce		json
//	@Param			q	query		string	false	"name search by q"	Format(email)
//	@Success		200	{array}		model.Account
//	@Failure		400	{object}	httputil.HTTPError
//	@Failure		404	{object}	httputil.HTTPError
//	@Failure		500	{object}	httputil.HTTPError
//	@Router			/accounts [get]
func (c *Controller) ListAccounts(ctx *gin.Context) {
	q := ctx.Request.URL.Query().Get("q")
	accounts, err := model.AccountsAll(q)
	if err != nil {
		httputil.NewError(ctx, http.StatusNotFound, err)
		return
	}
	ctx.JSON(http.StatusOK, accounts)
}

// AddAccount godoc
//
//	@Summary		Add an account
//	@Description	add by json account
//	@Tags			accounts
//	@Accept			json
//	@Produce		json
//	@Param			account	body		model.AddAccount	true	"Add account"
//	@Success		200		{object}	model.Account
//	@Failure		400		{object}	httputil.HTTPError
//	@Failure		404		{object}	httputil.HTTPError
//	@Failure		500		{object}	httputil.HTTPError
//	@Router			/accounts [post]
func (c *Controller) AddAccount(ctx *gin.Context) {
	var addAccount model.AddAccount
	if err := ctx.ShouldBindJSON(&addAccount); err != nil {
		httputil.NewError(ctx, http.StatusBadRequest, err)
		return
	}
	if err := addAccount.Validation(); err != nil {
		httputil.NewError(ctx, http.StatusBadRequest, err)
		return
	}
	account := model.Account{
		Name: addAccount.Name,
	}
	lastID, err := account.Insert()
	if err != nil {
		httputil.NewError(ctx, http.StatusBadRequest, err)
		return
	}
	account.ID = lastID
	ctx.JSON(http.StatusOK, account)
}

// UpdateAccount godoc
//
//	@Summary		Update an account
//	@Description	Update by json account
//	@Tags			accounts
//	@Accept			json
//	@Produce		json
//	@Param			id		path		int					true	"Account ID"
//	@Param			account	body		model.UpdateAccount	true	"Update account"
//	@Success		200		{object}	model.Account
//	@Failure		400		{object}	httputil.HTTPError
//	@Failure		404		{object}	httputil.HTTPError
//	@Failure		500		{object}	httputil.HTTPError
//	@Router			/accounts/{id} [patch]
func (c *Controller) UpdateAccount(ctx *gin.Context) {
	id := ctx.Param("id")
	aid, err := strconv.Atoi(id)
	if err != nil {
		httputil.NewError(ctx, http.StatusBadRequest, err)
		return
	}
	var updateAccount model.UpdateAccount
	if err := ctx.ShouldBindJSON(&updateAccount); err != nil {
		httputil.NewError(ctx, http.StatusBadRequest, err)
		return
	}
	account := model.Account{
		ID:   aid,
		Name: updateAccount.Name,
	}
	err = account.Update()
	if err != nil {
		httputil.NewError(ctx, http.StatusNotFound, err)
		return
	}
	ctx.JSON(http.StatusOK, account)
}

// DeleteAccount godoc
//
//	@Summary		Delete an account
//	@Description	Delete by account ID
//	@Tags			accounts
//	@Accept			json
//	@Produce		json
//	@Param			id	path		int	true	"Account ID"	Format(int64)
//	@Success		204	{object}	model.Account
//	@Failure		400	{object}	httputil.HTTPError
//	@Failure		404	{object}	httputil.HTTPError
//	@Failure		500	{object}	httputil.HTTPError
//	@Router			/accounts/{id} [delete]
func (c *Controller) DeleteAccount(ctx *gin.Context) {
	id := ctx.Param("id")
	aid, err := strconv.Atoi(id)
	if err != nil {
		httputil.NewError(ctx, http.StatusBadRequest, err)
		return
	}
	err = model.Delete(aid)
	if err != nil {
		httputil.NewError(ctx, http.StatusNotFound, err)
		return
	}
	ctx.JSON(http.StatusNoContent, gin.H{})
}

// UploadAccountImage godoc
//
//	@Summary		Upload account image
//	@Description	Upload file
//	@Tags			accounts
//	@Accept			multipart/form-data
//	@Produce		json
//	@Param			id		path		int		true	"Account ID"
//	@Param			file	formData	file	true	"account image"
//	@Success		200		{object}	controller.Message
//	@Failure		400		{object}	httputil.HTTPError
//	@Failure		404		{object}	httputil.HTTPError
//	@Failure		500		{object}	httputil.HTTPError
//	@Router			/accounts/{id}/images [post]
func (c *Controller) UploadAccountImage(ctx *gin.Context) {
	id, err := strconv.Atoi(ctx.Param("id"))
	if err != nil {
		httputil.NewError(ctx, http.StatusBadRequest, err)
		return
	}
	file, err := ctx.FormFile("file")
	if err != nil {
		httputil.NewError(ctx, http.StatusBadRequest, err)
		return
	}
	ctx.JSON(http.StatusOK, Message{Message: fmt.Sprintf("upload complete userID=%d filename=%s", id, file.Filename)})
}

```
### 浏览器中访问
http://116.204.108.126:8080/swagger/index.html
## 报错
> golang swagger internal server error doc.json
解决方法：
在main.go 中导入docs.go 
```go
import (
  _ "github.com/earthaYan/notePad/docs"
)
```