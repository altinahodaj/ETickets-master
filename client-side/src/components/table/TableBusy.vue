<template>
  <div class="table-loading">
    <b-spinner variant="primary" />
  </div>
</template>
<style lang="scss" scoped>
.table-loading {
  position: absolute;
  width: 100%;
  height: 100%;
  text-align: center;
  padding: 2rem;
  @media (min-width: 992px) {
    height: calc(100% - 66px);
    top: 66px;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 0;
  background: rgba($color: #fff, $alpha: 0.5);
  }
}
</style>
